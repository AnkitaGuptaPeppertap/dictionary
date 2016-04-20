from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form
from django.forms.fields import CharField, EmailField
from django.forms.widgets import PasswordInput

class AddUserForm(Form):
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    username = CharField(max_length=30)
    email = EmailField(required=False)
    password = CharField(max_length=30, widget=PasswordInput())
    confirm_password = CharField(max_length=30, widget=PasswordInput())

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username']) #get user from user model
        except User.DoesNotExist :
            return self.cleaned_data['username']

        raise ValidationError("This user exist already choose another username")

    def clean_email(self):
        if self.cleaned_data['email']:
            try:
                User.objects.get(email=self.cleaned_data['email']) #get user from user model
            except User.DoesNotExist :
                return self.cleaned_data['email']
            except Exception:
                raise ValidationError("This user exist already choose another email")

            raise ValidationError("This user exist already choose another email")
        else:
            return self.cleaned_data['email']

    def clean(self, *args , **kwargs):
        cleaned_data = super(AddUserForm, self).clean()
        if 'password' in cleaned_data and 'confirm_password' in cleaned_data:#check if both pass first validation
            if cleaned_data['password'] != cleaned_data['confirm_password']: # check if they match each other
                self._errors['confirm_password'] = self.error_class(["Passwords don't match each other"])
                self._errors['password'] = self.error_class(["Passwords don't match each other"])
                del cleaned_data['password']
                del cleaned_data['confirm_password']
                raise ValidationError("Passwords don't match each other")
        return cleaned_data

    def save(self, *args, **kwargs):
        new_user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password']
                                            ,email=self.cleaned_data['email'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
        return new_user