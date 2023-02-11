from tortoise import models, fields

from .country import Country

__all__ = [
    'City',
]


class City(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255,
                            unique=True,
                            index=True)
    country_id = fields.ForeignKeyField(model_name=Country.name,
                                        related_name='cities')

    def __str__(self) -> str:
        return self.name
