import datetime
import json
import num2words

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Customer, Invoice, UserProfile
from .utils import invoice_data_validator, invoice_data_processor

from .forms import UserForm


def landing_page(request):
    context = {}
    return render(request, 'gstbillingapp/pages/landing_page.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("invoice_create")
    context = {}
    auth_form = AuthenticationForm(request)
    if request.method == "POST":
        auth_form = AuthenticationForm(request, data=request.POST)
        if auth_form.is_valid():
            user = auth_form.get_user()
            if user:
                login(request, user)
                return redirect("invoice_create")
        else:
            context["error_message"] = auth_form.get_invalid_login_error()
    context["auth_form"] = auth_form
    return render(request, 'gstbillingapp/login.html', context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("invoice_create")
    context = {}
    signup_form = UserCreationForm()
    profile_edit_form = UserForm()
    context["signup_form"] = signup_form
    context["profile_edit_form"] = profile_edit_form

    if request.method == "POST":
        signup_form = UserCreationForm(request.POST)
        profile_edit_form = UserForm(request.POST)
        context["signup_form"] = signup_form
        context["profile_edit_form"] = profile_edit_form

        if signup_form.is_valid():
            user = signup_form.save()
        else:
            context["error_message"] = signup_form.errors
            return render(request, 'gstbillingapp/signup.html', context)
        if profile_edit_form.is_valid():
            userprofile = profile_edit_form.save(commit=False)
            userprofile.user = user
            userprofile.save()
            login(request,
                  user,
                  backend='django.contrib.auth.backends.ModelBackend')
            return redirect("invoice_create")

    return render(request, 'gstbillingapp/signup.html', context)


@login_required
def invoice_create(request):

    context = {}
    context['default_invoice_number'] = Invoice.objects.filter(
        user=request.user).aggregate(
            Max('invoice_number'))['invoice_number__max']
    if not context['default_invoice_number']:
        context['default_invoice_number'] = 1
    else:
        context['default_invoice_number'] += 1

    context['default_invoice_date'] = datetime.datetime.strftime(
        datetime.datetime.now(), '%Y-%m-%d')

    if request.method == 'POST':
        print("POST received - Invoice Data")

        invoice_data = request.POST

        validation_error = invoice_data_validator(invoice_data)
        if validation_error:
            context["error_message"] = validation_error
            return render(request, 'gstbillingapp/invoice_create.html',
                          context)

        print("Valid Invoice Data")

        invoice_data_processed = invoice_data_processor(invoice_data)

        customer = None

        try:
            customer = Customer.objects.get(
                user=request.user,
                customer_name=invoice_data['customer-name'],
                customer_address=invoice_data['customer-address'],
                customer_phone=invoice_data['customer-phone'],
                customer_gst=invoice_data['customer-gst'])
        except:
            print("===============> customer not found")
            print(invoice_data['customer-name'])
            print(invoice_data['customer-address'])
            print(invoice_data['customer-phone'])
            print(invoice_data['customer-gst'])

        if not customer:
            print("CREATING CUSTOMER===============>")
            customer = Customer(
                user=request.user,
                customer_name=invoice_data['customer-name'],
                customer_address=invoice_data['customer-address'],
                customer_phone=invoice_data['customer-phone'],
                customer_gst=invoice_data['customer-gst'])

            customer.save()

        invoice_data_processed_json = json.dumps(invoice_data_processed)
        new_invoice = Invoice(user=request.user,
                              invoice_number=int(
                                  invoice_data['invoice-number']),
                              invoice_date=datetime.datetime.strptime(
                                  invoice_data['invoice-date'], '%Y-%m-%d'),
                              invoice_customer=customer,
                              invoice_json=invoice_data_processed_json)
        new_invoice.save()
        print("INVOICE SAVED")

        return redirect('invoice_viewer', invoice_id=new_invoice.id)

    return render(request, 'gstbillingapp/invoice_create.html', context)


@login_required
def invoices(request):
    context = {}
    context['invoices'] = Invoice.objects.filter(
        user=request.user).order_by('-id')
    return render(request, 'gstbillingapp/invoices.html', context)


@login_required
def invoice_viewer(request, invoice_id):
    invoice_obj = get_object_or_404(Invoice, user=request.user, id=invoice_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    context = {}
    context['invoice'] = invoice_obj
    context['invoice_data'] = json.loads(invoice_obj.invoice_json)
    print(context['invoice_data'])
    context['currency'] = "₹"
    context['total_in_words'] = num2words.num2words(int(
        context['invoice_data']['invoice_total_amt_with_gst']),
                                                    lang='en_IN').title()
    context['user_profile'] = user_profile
    return render(request, 'gstbillingapp/invoice_printer.html', context)


@login_required
def invoice_delete(request):
    if request.method == "POST":
        invoice_id = request.POST["invoice_id"]
        invoice_obj = get_object_or_404(Invoice,
                                        user=request.user,
                                        id=invoice_id)

        invoice_obj.delete()
    return redirect('invoices')
