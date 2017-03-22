from django import forms

from django.contrib.auth import authenticate, get_user_model, get_user

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        
        
        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise forms.ValidationError("User doesn't exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("No longer active")
            
        return super(UserLoginForm, self).clean(*args, **kwargs)
        
class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'password',
            'password2',
            'email'
        ]
        
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(label="Email address")
    
    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Password must match")
        
        username = self.cleaned_data.get("username")
        username_qs = get_user_model().objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("This username has already been registered")
        
        email = self.cleaned_data.get("email")
        email_qs = get_user_model().objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        return super(UserRegisterForm, self).clean(*args, **kwargs)
    