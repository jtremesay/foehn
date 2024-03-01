import uuid

from django.db import models


class Farm(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name or "<Unamed {}(uuid={})>".format(
            self.__class__.name, self.uuid
        )
