class Loader:

    factoryStore = dict()
    loadStore = dict()

    @classmethod
    def register(cls, key, factory):
        cls.factoryStore[key] = factory
    
    @classmethod
    def create(cls, key):
        loader = cls.loadStore.get(key)
        if not loader:
            factory = cls.factoryStore.get(key)
            loader = factory.create()
        return loader

    def load(self, path):
        print('no method')
