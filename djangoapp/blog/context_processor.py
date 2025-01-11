from blog.models import SiteSetup


def site_setup(request):
    data = SiteSetup.objects.order_by('-id').first()
    return {
        'site_setup': data
    }
