from django.shortcuts import render
from agenda.models import Contact
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    contacts = Contact.objects \
        .filter(show=True)\
        .order_by('-id')

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Contacts'
    }
    return render(
        request,
        'agenda/pages/index.html',
        context
    )
