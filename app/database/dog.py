import datetime

import mongoengine as me


class DogDocument(me.Document):
    name = me.StringField(required=True, max_length=100, unique=True)
    breed = me.StringField(max_length=100)
    features = me.ListField()
    creation_date = me.DateTimeField()
    modified_date = me.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(DogDocument, self).save(*args, **kwargs)
