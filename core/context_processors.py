from django.conf import settings

def social_settings(request):
    """
    Context processor to make social contact settings available in templates.
    """
    return {
        'settings': {
            'WHATSAPP_PHONE_NUMBER': getattr(settings, 'WHATSAPP_PHONE_NUMBER', '971501234567'),
            'INSTAGRAM_USERNAME': getattr(settings, 'INSTAGRAM_USERNAME', 'roseandivyflowers'),
        }
    }
