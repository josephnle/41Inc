from django.shortcuts import render
import account.views
import websites.forms
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth, messages

# Create your views here.

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
        user = auth.authenticate(request = self.request, **self.user_credentials())
        auth.login(self.request, user)
        self.request.session.set_expiry(0)

    def get_form_kwargs(self):
        kw = super(WebsiteSignupView, self).get_form_kwargs()
        kw['request'] = self.request  # the trick!
        return kw
