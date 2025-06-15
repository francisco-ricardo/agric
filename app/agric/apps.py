from django.apps import AppConfig

import logging
logger = logging.getLogger(__name__)


class AgricConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agric'

    def ready(self):        
        logger.info("App 'agric' inicializado.")