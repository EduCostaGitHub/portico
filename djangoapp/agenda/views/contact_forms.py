from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse


from agenda.forms import ContactForm
from agenda.models import Contact


@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('agenda:create')

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)

        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            # print('form is valid')
            # contact = form.save()
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            # contact.show = True

            # valid form, redirect to update
            return redirect('agenda:update', contact_id=contact.pk)

        return render(
            request,
            'contact/create.html',
            context
        )

    context = {
        'form': ContactForm(),
        'form_action': form_action,
    }

    return render(
        request,
        'agenda/pages/create.html',
        context
    )


@login_required(login_url='agenda:login')
def update(request, contact_id):
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user)
    form_action = reverse('agenda:update', args=(contact_id,))

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            contact = form.save()
            return redirect('agenda:update', contact_id=contact.pk)

        return render(
            request,
            'agenda/pages/create.html',
            context
        )

    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action,
    }

    return render(
        request,
        'agenda/pages/create.html',
        context
    )


@login_required(login_url='agenda:login')
def delete(request, contact_id):
    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user)

    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        contact.delete()
        return redirect('agenda:index')

    # contact.delete()
    # return redirect('contact:index')
    return render(
        request,
        'agenda/pages/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation
        }
    )
