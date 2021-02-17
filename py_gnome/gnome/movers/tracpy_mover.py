#!/usr/bin/env python

"""
simple_mover.py

This is an example mover class -- not really useful, but about as simple as
can be, for testing and demonstration purposes

It's a steady, uniform current -- one velocity and direction for everywhere
at all time.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import copy

import numpy as np
from numpy.random import uniform

from gnome import basic_types
from gnome.utilities.projections import FlatEarthProjection as proj
from gnome.utilities import serializable

from gnome.movers import Mover


class SimpleMover(Mover, serializable.Serializable):
    """
    simple_mover

    a really simple mover -- moves all LEs a constant speed and direction

    (not all that different than a constant wind mover, now that I think
     about it)
    """

    _state = copy.deepcopy(Mover._state)
    _state.add(update=['uncertainty_scale', 'velocity'],
               save=['uncertainty_scale', 'velocity'])

    def __init__(self, velocity, uncertainty_scale=0.5,
                 **kwargs):
        """
        simple_mover (velocity)

        create a simple_mover instance

        :param velocity: a (u, v, w) triple -- in meters per second

        Remaining kwargs are passed onto Mover's __init__ using super.
        See Mover documentation for remaining valid kwargs.
        """
        # use this, to be compatible with whatever we are using for location
        self.velocity = (np.asarray(velocity, dtype=basic_types.mover_type)
                         .reshape((3,)))

        self.uncertainty_scale = uncertainty_scale

        super(SimpleMover, self).__init__(**kwargs)

    def __repr__(self):
        return 'SimpleMover(<%s>)' % self.id

    def velocity_to_dict(self):
        """
        convert velocity back into a tuple
        """

        return tuple(self.velocity.tolist())

    def get_move(self, spill, time_step, model_time,):
        """
        moves the particles defined in the spill object

        :param spill: spill is an instance of the gnome.spill.Spill class
        :param time_step: time_step in seconds
        :param model_time: current model time as a datetime object
        In this case, it uses the:
            positions
            status_code
        data arrays.

        :returns delta: Nx3 numpy array of movement -- in (long, lat, meters)
                        units
        """
        # Get the data:

        try:
            positions = spill['positions']
            status_codes = spill['status_codes']
        except KeyError as err:
            raise ValueError('The spill does not have the required '
                             'data arrays\n{}'
                             .format(err))

        # which ones should we move?
        in_water_mask = status_codes == basic_types.oil_status.in_water

        # compute the move
        delta = np.zeros_like(positions)

        if self.active and self.on:
            delta[in_water_mask] = self.velocity * time_step

            # add some random stuff if uncertainty is on
            if spill.uncertain:
                num = sum(in_water_mask)
                scale = self.uncertainty_scale * self.velocity * time_step

                delta[in_water_mask, 0] += uniform(-scale[0], scale[0], num)
                delta[in_water_mask, 1] += uniform(-scale[1], scale[1], num)
                delta[in_water_mask, 2] += uniform(-scale[2], scale[2], num)

            # scale for projection
            # just the lat-lon...
            delta = proj.meters_to_lonlat(delta, positions)

        return delta
