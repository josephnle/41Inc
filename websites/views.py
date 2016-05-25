import account.views
import datetime
import stripe
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
import json
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView
from django.shortcuts import render

from fourtyone import settings
from websites.mixins import PremiumEnabledMixin
import websites.forms
from series.models import Series
from subscriptions.models import Settings as SubscriptionSettings, Subscription


class SubscribeView(PremiumEnabledMixin, TemplateView):
    template_name = 'websites/payments/subscribe.html'

    def get_context_data(self, **kwargs):
        context = super(SubscribeView, self).get_context_data(**kwargs)

        # Get current site
        current_site = get_current_site(self.request)

        # Get prices
        site = SubscriptionSettings.objects.get(pk=current_site.id)

        context['price_month'] = site.price_month
        context['price_year'] = site.price_year

        return context

    def post(self, request, *args, **kwargs):
        # Import API key
        stripe.api_key = settings.STRIPE_CLIENT_SECRET

        # Get current site ID
        site = get_current_site(request)

        # Import site's API key
        stripe_account = SubscriptionSettings.objects.get(pk=site.id).stripe_user_id

        # Get token from request
        token = request.POST['token']

        # Create Stripe customer
        customer = stripe.Customer.create(
            source=token,
            plan=settings.PLAN_ID_MONTHLY,
            stripe_account=stripe_account
        )

        # Create new subscription
        Subscription(customer_id=customer.id, user=request.user, site=site,
                     active_until=timezone.make_aware(datetime.datetime.fromtimestamp(
                         int(customer.subscriptions.data[0].current_period_end)))).save()

        return HttpResponse('Subscription created.')


class WebsiteSignupView(account.views.SignupView):
    form_class = websites.forms.SignupForm

    def after_signup(self, form):
        # Update first/last name
        self.created_user.first_name = form.cleaned_data["first_name"]
        self.created_user.last_name = form.cleaned_data["last_name"]
        self.created_user.save()

        # Create profile
        self.create_profile(form)

        super(WebsiteSignupView, self).after_signup(form)

    def create_profile(self, form):
        profile = self.created_user.profile
        profile.company = form.cleaned_data["company"]
        profile.site = get_current_site(self.request)
        profile.save()

    def login_user(self):
        user = auth.authenticate(request=self.request, **self.user_credentials())
        auth.login(self.request, user)
        self.request.session.set_expiry(0)

    def get_form_kwargs(self):
        kw = super(WebsiteSignupView, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw


def site_homepage(request):
    series_for_site = Series.objects.all()
    context = {'series_for_site': series_for_site}
    return render(request, 'websites/homepage.html', context)
