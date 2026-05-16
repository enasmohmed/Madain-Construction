from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import FormView

from .forms import ContactForm
from .services import submit_contact_message


class ContactFormView(FormView):
    template_name = "contact/contact_form.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_form")

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            submit_contact_message(
                name=data["name"],
                email=data["email"],
                subject=data["subject"],
                message=data["message"],
            )
        except Exception:
            messages.error(
                self.request,
                _("We could not send your message. Please try again later."),
                extra_tags="contact",
            )
            return self.form_invalid(form)

        messages.success(
            self.request,
            _("Your message was sent successfully. We will get back to you soon."),
            extra_tags="contact",
        )
        return super().form_valid(form)
