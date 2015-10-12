class Resources:

    names = ['fighters', 'rogues', 'wizards', 'clerics', 'vp']

    def __init__(self, **kwargs):
        for name in self.names:
            setattr(self, name, kwargs.get(name, 0))

    def __add__(left, right):
        result = Resources()
        for name in left.names:
            setattr(result, name, getattr(left, name) + getattr(right, name))
        return result

    def __sub__(left, right):
        result = Resources()
        for name in left.names:
            setattr(result, name, getattr(left, name) - getattr(right, name))
        return result

    def __repr__(self):
        items = ['{}: {}'.format(name, getattr(self, name))
                 for name in self.names]
        return ', '.join(items)


class QualityResources(Resources):
    names = ['quests', 'intrigues']
