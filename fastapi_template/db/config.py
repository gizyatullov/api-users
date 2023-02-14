from typing import List

from fastapi_template.settings import settings

MODELS_MODULES: List[str] = [
    'fastapi_template.db.models.user',
    'fastapi_template.db.models.country',
    'fastapi_template.db.models.city',
    'fastapi_template.db.models.category',
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
