from collections import OrderedDict


class NavigationTree(object):
    """
    An object that renders a JSON representation of a `py_gnome.model.Model`
    used to initialize a navigation tree widget in the JavaScript app.
    """
    def __init__(self, model):
        self.model = model

    def _get_model_settings(self):
        """
        Return a dict of values containing each model setting that the client
        should be able to read and change.
        """
        settings_attrs = [
            'start_time',
            'duration'
        ]

        settings = OrderedDict()

        for attr in settings_attrs:
            if hasattr(self.model, attr):
                settings[attr] = getattr(self.model, attr)

        return settings

    def _get_value_title(self, name, value, max_chars=8):
        """
        Return a title string that combines `name` and `value`, with value
        shortened if it is longer than `max_chars`.
        """
        name = name.replace('_', ' ').title()
        value = (str(value)).title()
        value = value if len(value) <= max_chars else '%s ...' % value[:max_chars]
        return '%s: %s' % (name, value)

    def render(self):
        """
        Return an ordered list of tree elements, suitable for JSON serialization.
        """
        settings = {'title': 'Model Settings', 'type': 'settings', 'children': []}
        movers = {'title': 'Movers', 'type': 'add_mover', 'children': []}
        spills = {'title': 'Spills', 'type': 'add_spill', 'children': []}

        for name, value in self._get_model_settings().items():
            settings['children'].append({
                'type': 'settings',
                'title': self._get_value_title(name, value),
            })

        # If we had a map, we would set its ID value here, whatever that value
        # ends up being.
        settings['children'].append({
            'type': 'map',
            'title': 'Map: None'
        })

        for mover in self.model.movers:
            movers['children'].append({
                'type': mover.name,
                'id': mover.id,
                'title': str(mover)
            })

        for spill in self.model.spills:
            spills['children'].append({
                'type': spill.name,
                'id': spill.id,
                'title': self._get_value_title('ID', id),
            })

        return [settings, movers, spills]
