import logging
import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerpath.settings")

application = get_wsgi_application()

render_host = "career-guidance-for-10th-students.onrender.com"
logging.getLogger("careerpath").info(
    "Django startup configuration: settings_module=%s, DEBUG=%s, "
    "Render host allowed=%s, Render host entry count=%d, ALLOWED_HOSTS count=%d",
    os.environ["DJANGO_SETTINGS_MODULE"],
    settings.DEBUG,
    render_host in settings.ALLOWED_HOSTS,
    settings.ALLOWED_HOSTS.count(render_host),
    len(settings.ALLOWED_HOSTS),
)
