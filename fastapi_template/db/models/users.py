from tortoise import Model, fields

from fastapi_template import shemas

__all__ = [
    "Users",
]


class Users(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    password = fields.BinaryField()
    role_name = fields.CharEnumField(enum_type=shemas.UserRole)
    is_seller = fields.BooleanField(default=False)
    jwt_key = fields.CharField(max_length=255, null=True)
    btc_balance = fields.FloatField(null=True)
    btc_address = fields.CharField(max_length=255, null=True)
    otp = fields.CharField(max_length=255, null=True)
    city = fields.CharField(max_length=255, null=True)
    avatar = fields.CharField(max_length=255, null=True)
    created = fields.DatetimeField(auto_now_add=True)
    is_banned = fields.BooleanField(default=False)
    user_ban_date = fields.DatetimeField(null=True)

    def __str__(self):
        return f"{self.username} | {self.role_name}"
