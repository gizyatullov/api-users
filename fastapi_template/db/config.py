from typing import List

from fastapi_template.settings import settings

MODELS_MODULES: List[str] = [
    'fastapi_template.db.models.dummy_model',
    'fastapi_template.db.models.user',
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
