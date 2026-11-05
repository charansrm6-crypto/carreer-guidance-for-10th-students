from django.conf import settings


def whatsapp_group_url(request):
    return {"whatsapp_group_url": getattr(settings, "WHATSAPP_GROUP_URL", "")}
