from .dog import DogDocument


class DogRepository:
    def __init__(self):
        self.collection = DogDocument

    def save(self, data):
        dog = self.collection(name=data.name, breed=data.breed, features=data.features)
        dog.save()
        return dog

    def get_by_name(self, name):
        dog = self.collection.objects(name=name).first()
        return dog

    def update_by_name(self, row: object, data: object):
        row.name = data.name
        row.breed = data.breed
        row.features = data.features
        row.save()
        return row

    def get_all(self):
        return self.collection.objects()
