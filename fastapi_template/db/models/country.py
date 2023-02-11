from tortoise import models, fields

__all__ = [
    'Country',
]


class Country(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255,
                            unique=True,
                            index=True)

    class Meta:
        table = 'countries'

    def __str__(self) -> str:
        return self.name
