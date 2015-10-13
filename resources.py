class Resources:

    names = ['fighters', 'rogues', 'wizards', 'clerics', 'gold', 'vp']

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
    names = ['quests', 'buildings', 'intrigues']

    def only_faceup(self):
        return QualityResources(quests=self.quests, buildings=self.buildings)

    def only_facedown(self):
        return QualityResources(intrigues=self.intrigues)
