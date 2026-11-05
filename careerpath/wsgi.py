import logging
import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerpath.settings")

application = get_wsgi_application()

render_hosts = {
    "carreer-guidance-for-10th-students.onrender.com",
    "career-guidance-for-10th-students.onrender.com",
}
logging.getLogger("careerpath").info(
    "Django startup configuration: settings_module=%s, DEBUG=%s, "
    "Render host allowed=%s, Render host entry count=%d, ALLOWED_HOSTS count=%d",
    os.environ["DJANGO_SETTINGS_MODULE"],
    settings.DEBUG,
    any(host in render_hosts for host in settings.ALLOWED_HOSTS),
    sum(1 for host in settings.ALLOWED_HOSTS if host in render_hosts),
    len(settings.ALLOWED_HOSTS),
)
