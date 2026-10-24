import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import ContactMessage

Student = get_user_model()


class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}), min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}), min_length=8)

    class Meta:
        model = Student
        fields = ["full_name", "email", "class_name", "phone_number", "password"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "class_name": forms.Select(attrs={"class": "form-select"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Phone Number"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if Student.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered. Please use a different email.")
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"].strip()
        if not full_name:
            raise forms.ValidationError("Enter your full name.")
        return full_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"].strip()
        if not re.fullmatch(r"\+?[0-9 ().-]{7,20}", phone_number):
            raise forms.ValidationError("Enter a valid phone number.")
        digit_count = sum(character.isdigit() for character in phone_number)
        if not 7 <= digit_count <= 15:
            raise forms.ValidationError("Enter a phone number with 7 to 15 digits.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        if password:
            try:
                validate_password(password, user=Student(
                    full_name=cleaned_data.get("full_name", ""),
                    email=cleaned_data.get("email", ""),
                ))
            except ValidationError as error:
                self.add_error("password", error)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = user.email
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Your Email"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Write your message here"}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Enter your name.")
        return name

    def clean_email(self):
        return self.cleaned_data["email"].strip()

    def clean_subject(self):
        subject = self.cleaned_data["subject"].strip()
        if not subject:
            raise forms.ValidationError("Enter a subject.")
        return subject

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if not message:
            raise forms.ValidationError("Enter a message.")
        return message
