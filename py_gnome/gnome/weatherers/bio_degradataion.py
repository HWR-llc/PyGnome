﻿'''
model biodegradation process
'''
import numpy as np

from gnome.utilities.serializable import Serializable

from .core import WeathererSchema
from gnome.weatherers import Weatherer

from gnome.array_types import (mass, 
                               droplet_avg_size)

from math import exp, pi

class Biodegradation(Weatherer, Serializable):
    _state = copy.deepcopy(Weatherer._state)
    _state += [Field('water', save=True, update=True, save_reference=True),
               Field('waves', save=True, update=True, save_reference=True)]

    _schema = WeathererSchema

    def __init__(self, waves=None, water=None, **kwargs):
        self.waves = waves
        self.water = water

        super(Biodegradation, self).__init__(**kwargs)

        self.array_types.update({'area': area,
                                 'mass':  mass,
                                 'droplet_avg_size': droplet_avg_size
                                 })


    def prepare_for_model_run(self, sc):
        '''
            Add biodegradation key to mass_balance if it doesn't exist.
            - Assumes all spills have the same type of oil
            - let's only define this the first time
        '''
        if self.on:
            super(Biodegradation, self).prepare_for_model_run(sc)
            sc.mass_balance['bio_degradation'] = 0.0

    def prepare_for_model_step(self, sc, time_step, model_time):
        '''
            Set/update arrays used by dispersion module for this timestep
        '''
        super(Biodegradation, self).prepare_for_model_step(sc, time_step, model_time)

        if not self.active:
            return


    def bio_degradate_oil(self, data, substance, **kwargs):
        '''
            1. Droplet distribution per LE should be calculated by the natural
            dispersion process and saved in the data arrays before the 
            biodegradation weathering process.
            2. It must take into consideration saturates and aromatic mass fractions only.
        '''

        model_time = kwargs.get('model_time')
        time_step = kwargs.get('time_step')

        comp_masses = data['mass_components']
        droplet_avg_sizes = data['droplet_avg_size']

        # we are going to calculate bio degradation rate coefficients (K_comp_rate) 
        # just for saturate and aromatics components - other ones are masked to 0.0

        K_comp_rates = get_K_comp_rates(substance)

        mass_biodegradated = comp_masses * exp(-4.0 * pi * droplet_avg_sizes ** 2 * 
                                               K_comp_rate * time_step / 
                                               comp_masses.sum(axes=1))

        # TODO

    def get_K_val(self, type_and_bp, arctic = False):
        '''
            Get bio degradation rate coefficient based on component type and 
            its boiling point for temparate or arctic environment conditions
            type_and_bp: a tuple ('type', 'boiling_point')
                - 'type': component type, string
                - 'boiling_point': float value
            arctic: flag for arctic conditions ( below 6 deg C)
        '''

        if type_and_bp[0] == 'Saturates':
            if type_and_bp[1] < 722.85:     # 722.85 - boiling point for C30 saturate (K)
                return 0.128807242 if arctic else 0.941386396
            else:
                return 0.0                  # no coefficients for C30 and above saturates

        elif type_and_bp[1] == 'Aromatics':
            if type_and_bp[1] < 630.0:      # 
                return 0.126982603 if arctics else 0.575541103
            else:
                return 0.021054707 if arctics else 0.084840485
        else:
            return 0.0
        

    def get_K_comp_rates(self, substance, arctic = False):
        '''
            Calculate bio degradation rate coefficient for each oil component
            We calculate ones just for saturates below C30 and aromatics
            Also they are coming for two environment conditions arctic or temperate 
        '''

        assert 'boiling_point' in substance._sara.dtype.names

        type_bp = substance._sara[['type','boiling_point']]     # 

        return np.array(map(get_K_val, type_bp)


    def weather_elements(self, sc, time_step, model_time):
        '''
            weather elements over time_step
        '''
        if not self.active:
            return

        if sc.num_released == 0:
            return

        for substance, data in sc.itersubstancedata(self.array_types):
            if len(data['mass']) is 0:
                continue

            bio_deg = self.bio_degradate_oil(model_time=model_time,
                                             time_step=time_step,
                                             data=data,
                                             substance=substance)

            data['mass_components'] -= bio_deg

            sc.mass_balance['bio_degradation'] += bio_deg.sum()

            data['mass'] = data['mass_components'].sum(1)

            # log bio degradated amount
            self.logger.debug('{0} Amount bio degradated for {1}: {2}'
                              .format(self._pid,
                                      substance.name,
                                      sc.mass_balance['bio_degradation']))

        sc.update_from_fatedataview()


    def serialize(self, json_='webapi'):
        """
            'water'/'waves' property is saved as references in save file
        """
        toserial = self.to_serialize(json_)
        schema = self.__class__._schema()
        serial = schema.serialize(toserial)

        if json_ == 'webapi':
            if self.waves:
                serial['waves'] = self.waves.serialize(json_)
            if self.water:
                serial['water'] = self.water.serialize(json_)

        return serial

    @classmethod
    def deserialize(cls, json_):
        """
            Append correct schema for water
        """
        if not cls.is_sparse(json_):
            schema = cls._schema()
            dict_ = schema.deserialize(json_)

            if 'water' in json_:
                obj = json_['water']['obj_type']
                dict_['water'] = (eval(obj).deserialize(json_['water']))

            if 'waves' in json_:
                obj = json_['waves']['obj_type']
                dict_['waves'] = (eval(obj).deserialize(json_['waves']))

            return dict_
        else:
            return json_
