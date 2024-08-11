from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post, Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        # Exclude 'author' from the form fields as it will be set in the view

    # Custom validation or additional fields can be added here if needed
    # Example:
    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if len(title) < 5:
    #         raise forms.ValidationError("Title must be at least 5 characters long.")
    #     return title

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    # Additional custom validation or customization can be added here if needed
    # Example:
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     # Add any custom validation logic
    #     return username

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Name',
        widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 4, 'class': 'form-control'}),
        label='Message'
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # Ensure Profile model exists
        fields = ['bio', 'profile_picture']  # Ensure these fields exist in the Profile model

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # You can add additional customization here if needed
        self.fields['profile_picture'].required = False  # Example: make profile picture optional

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # 'password1' and 'password2' are provided by UserCreationForm
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
