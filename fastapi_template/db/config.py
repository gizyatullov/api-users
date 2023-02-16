from typing import List

from fastapi_template.settings import settings

MODELS_MODULES: List[str] = [
    'aerich.models',
    'fastapi_template.db.models.user',
    'fastapi_template.db.models.country',
    'fastapi_template.db.models.city',
    'fastapi_template.db.models.category',
    'fastapi_template.db.models.subcategory',
]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    'connections': {
        'default': str(settings.db_url),
    },
    'apps': {
        'models': {
            'models': MODELS_MODULES,
            'default_connection': 'default',
        },
    },
}
