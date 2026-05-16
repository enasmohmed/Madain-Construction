from django import forms
from django.utils.translation import gettext_lazy as _

INPUT_CLASS = "simply-contact__input"
TEXTAREA_CLASS = "simply-contact__textarea"


class HomeContactForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": _("Your Name"),
                "autocomplete": "name",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": _("Email Address"),
                "autocomplete": "email",
            }
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": TEXTAREA_CLASS,
                "placeholder": _("Your Message"),
                "rows": 4,
            }
        ),
    )


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": INPUT_CLASS, "placeholder": _("Your Name")}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": INPUT_CLASS, "placeholder": _("Email Address")}
        ),
    )
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": INPUT_CLASS, "placeholder": _("Subject")}
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": TEXTAREA_CLASS,
                "placeholder": _("Your Message"),
                "rows": 5,
            }
        ),
    )
