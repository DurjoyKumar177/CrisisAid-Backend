from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        """
        Send custom email verification using accounts/templates/email_confirmation.html
        """
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": f"{settings.FRONTEND_URL}/verify-email/{emailconfirmation.key}/",
            "key": emailconfirmation.key,
            "current_site": request.get_host(),
        }

        subject = "Verify your email - Crisis Aid"
        from_email = settings.EMAIL_HOST_USER
        recipient = [emailconfirmation.email_address.email]

        # Render HTML and plain text versions
        html_content = render_to_string("email_confirmation.html", ctx)
        text_content = render_to_string("email_confirmation.txt", ctx) if \
                       self.template_exists("email_confirmation.txt") else \
                       f"Please verify your email by visiting: {ctx['activate_url']}"

        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def template_exists(self, template_name):
        """Check if a template exists to avoid errors."""
        from django.template import engines
        try:
            engines['django'].engine.get_template(template_name)
            return True
        except:
            return False


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Prevent duplicate accounts if Google login email already exists.
        """
        if sociallogin.is_existing:
            return

        email = sociallogin.user.email
        if email:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                existing_user = User.objects.get(email=email)
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass
