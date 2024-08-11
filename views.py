from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import ContactForm, ProfileForm, PostForm, RegistrationForm
from .models import Post, Profile

def homepage(request):
    """View function for the homepage."""
    return render(request, 'social_media/home.html')

def home(request):
    """View function for the home page with all posts."""
    posts = Post.objects.all()
    return render(request, 'social_media/home.html', {'posts': posts})

def about(request):
    """View function for the about page."""
    return render(request, 'social_media/about.html')

def contact(request):
    """View function for the contact page with form handling."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                subject=f'Contact Form Submission from {name}',
                message=message,
                from_email=email,
                recipient_list=['your_email@example.com'],  # Replace with your email
                fail_silently=False,
            )
            return redirect('social_media:contact')
    else:
        form = ContactForm()
    return render(request, 'social_media/contact.html', {'form': form})

def login(request):
    """View function for the login page."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('social_media:home')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'social_media/login.html', {'form': form})

@login_required
def create_post(request):
    """View function for creating a new post."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('social_media:post_list')
    else:
        form = PostForm()
    return render(request, 'social_media/create_post.html', {'form': form})

def register(request):
    """View function for the registration page."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('social_media:login')
    else:
        form = RegistrationForm()
    return render(request, 'social_media/register.html', {'form': form})

@login_required
def logout(request):
    """View function for logout."""
    auth_logout(request)
    return redirect('social_media:home')

@login_required
def profile(request):
    """View function for the user profile page."""
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(instance=profile)
    return render(request, 'social_media/profile.html', {'profile': profile, 'form': form})

@login_required
def update_profile(request):
    """View function for updating the user profile."""
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('social_media:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'social_media/update_profile.html', {'form': form})

def view_post(request, post_id):
    """View function for displaying a specific post."""
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'social_media/view_post.html', {'post': post})

@login_required
def update_post(request, post_id):
    """View function for updating a specific post."""
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('social_media:view_post', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'social_media/update_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    """View function for deleting a specific post."""
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('social_media:home')
    return render(request, 'social_media/delete_post.html', {'post': post})

def post_list(request):
    """View function for displaying a list of all posts."""
    posts = Post.objects.all()
    return render(request, 'social_media/post_list.html', {'posts': posts})
