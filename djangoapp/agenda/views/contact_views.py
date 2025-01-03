from django.shortcuts import render, get_object_or_404
from agenda.models import Contact
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    contacts = Contact.objects \
        .filter(show=True) \
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


def search(request):
    search_value = request.GET.get('q', '').strip()

    if search_value == '':
        return redirect('agenda:index')

    contacts = Contact.objects \
        .filter(show=True)\
        .filter(
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(phone__icontains=search_value) |
            Q(email__icontains=search_value),
        )\
        .order_by('-id')

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'search'
    }

    return render(
        request,
        'agenda/pages/index.html',
        context
    )


def contact(request, contact_id):
    # single_contact = Contact.objects.filter(pk=contact_id).first()
    single_contact = get_object_or_404(Contact, pk=contact_id, show=True)

    # if single_contact is None:
    #    raise Http404('Contact Not Found!')

    context = {
        'contact': single_contact,
        'site_title': single_contact.first_name

    }

    return render(
        request,
        'agenda/pages/contact.html',
        context
    )
