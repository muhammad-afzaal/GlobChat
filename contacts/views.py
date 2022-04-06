from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from contacts import utility_functions
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect, get_object_or_404
from django.db import models, IntegrityError
from django.contrib.auth.models import User
from contacts.models import Contact


@login_required()
def contacts(request):
    contacts_ = utility_functions.get_contacts(request)
    return render(request, 'contacts.html', {'users': contacts_, 'len_contacts': len(contacts_)})


@login_required()
def addable_contacts(request):
    user = get_user_model()
    return render(request, 'add-contact.html', {'users': utility_functions.get_addable_users(request)})


@login_required
def add_contact(request):
    other_username = request.POST.get("other_username")
    other_user = User.objects.get(username=other_username)

    if len(Contact.objects.all().filter(owner=request.user).filter(other=other_user)) == 0:
        Contact.add_this(Contact(), request.user, other_user)
    return contacts(request)


@login_required
def remove_contact(request):
    other_username = request.POST.get("other_username")
    other_user = User.objects.get(username=other_username)
    Contact.objects.filter(owner=request.user).filter(other=other_user).delete()
    return contacts(request)
