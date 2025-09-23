
import os
from django.core.wsgi import get_wsgi_application  # CORRECTO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria.settings')

application = get_wsgi_application()
