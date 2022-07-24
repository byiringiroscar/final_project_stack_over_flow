from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from authentication.models import Profile
from django.core.exceptions import ValidationError

User = get_user_model()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, error_messages={'password': 'password must match'})
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput,
                                 error_messages={'password': 'password must match'})

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password', 'password_2']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_phone(self):
        '''
        Verify phone is available.
        '''
        phone_number = self.cleaned_data.get('phone_number')
        qs = User.objects.filter(phone_number=phone_number, is_verified=True)
        if qs.exists():
            raise forms.ValidationError("phone number  is taken")

        return phone_number

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """
            A form for creating new users. Includes all the required
            fields, plus a repeated password.
            """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
            the user, but replaces the password field with admin's
            password hash display field.
            """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_image', 'location', 'about_me', 'github_link', 'website_link', ]


class UpdateProfileForm(forms.ModelForm):
    user_image = forms.ImageField(label='Profile picture', required=False)
    location = forms.CharField(label='ID number', required=False)
    github_link = forms.URLField(label="Git hub link", required=False)
    website_link = forms.URLField(label="Website link", required=False)

    class Meta:
        model = Profile
        fields = ['user_image', 'location', 'about_me', 'github_link', 'website_link', ]


class SkillsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['backend_development', 'frontend_development', 'hardware', 'uiandux', 'artificial_intelligence', ]

    def clean_backend_development(self):
        backend_development = self.cleaned_data['backend_development']
        if backend_development:
            if backend_development > 100:
                raise ValidationError("number must not be greater than 100")
            if isinstance(backend_development, float):
                raise ValidationError("please use positive number only")
            if backend_development < 0:
                raise ValidationError("please use positive number only")
            return backend_development
        else:
            return 0

    def clean_frontend_development(self):
        frontend_development = self.cleaned_data['frontend_development']
        if frontend_development:
            if frontend_development > 100:
                raise ValidationError("number must not be greater than 100")
            if isinstance(frontend_development, float):
                raise ValidationError("please use positive number only")
            if frontend_development < 0:
                raise ValidationError("please use positive number only")
            return frontend_development
        else:
            return 0

    def clean_hardware(self):
        hardware = self.cleaned_data['hardware']
        if hardware:
            if hardware > 100:
                raise ValidationError("number must not be greater than 100")
            if isinstance(hardware, float):
                raise ValidationError("please use positive number only")
            if hardware < 0:
                raise ValidationError("please use positive number only")
            return hardware
        else:
            return 0

    def clean_uiandux(self):
        uiandux = self.cleaned_data['uiandux']
        if uiandux:
            if uiandux > 100:
                raise ValidationError("number must not be greater than 100")
            if isinstance(uiandux, float):
                raise ValidationError("please use positive number only")
            if uiandux < 0:
                raise ValidationError("please use positive number only")
            return uiandux
        else:
            return 0

    def clean_artificial_intelligence(self):
        artificial_intelligence = self.cleaned_data['artificial_intelligence']
        if artificial_intelligence:
            if artificial_intelligence > 100:
                raise ValidationError("number must not be greater than 100")
            if isinstance(artificial_intelligence, float):
                raise ValidationError("please use positive number only")
            if artificial_intelligence < 0:
                raise ValidationError("please use positive number only")
            return artificial_intelligence
        else:
            return 0
