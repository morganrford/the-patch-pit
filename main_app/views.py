from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Distro, Patch
from main_app.models import Distro, Patch
from django.http import Http404
from .forms import PatchForm, UserForm, UserUpdateForm
from main_app.forms import UploadForm, PatchForm, LoginForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    patches = Patch.objects.all()
    return render(request, 'home.html', {'patches': patches})

def about(request):
    return render(request, 'about.html')

def distro_index(request):
    distros = Distro.objects.all()
    return render(request, 'distros/index.html', {'distros': distros})

def distro_detail(request, distro_id):
    distro = Distro.objects.get(id=distro_id)
    patch_form = PatchForm()
    return render(request, 'distros/detail.html', {'distro': distro, 'patch_form': patch_form})

class DistroCreate(LoginRequiredMixin, CreateView):
    model = Distro
    fields = ['name', 'photo', 'website', 'description']
    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class DistroUpdate(UpdateView):
    model = Distro
    fields = ['website', 'description']

class DistroDelete(DeleteView):
    model = Distro
    success_url = '/distros/'
    
def patch_index(request):
    patches = Patch.objects.all()
    return render(request, 'patches/index.html', {'patches': patches})

def patch_detail(request, patch_id):
    patch = Patch.objects.get(id=patch_id)
    return render(request, 'patches/detail.html', {'patch': patch})

class PatchCreate(LoginRequiredMixin, CreateView):
    model = Patch
    fields = ['name', 'photo', 'link', 'description']
    success_url = '/patches/'
    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class PatchUpdate(UpdateView):
    model = Patch
    fields = '__all__'

class PatchDelete(DeleteView):
    model = Patch
    success_url = '/patches/'

def distro_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('distro_index')
    else:
        form = UploadForm()
    
    return render(request, 'main_app/distro_form.html', {'form': form})

def patch_upload(request):
    if request.method == 'POST':
        form = PatchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('patch_index')
    else:
        form = PatchForm()
    
    return render(request, 'main_app/patch_form.html', {'form': form})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again!'
    form = UserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

def signout_view(request):
    logout(request)
    return redirect('home')

def signin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm()  
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            print(f"User is not none")
            return redirect('home')
    error_message = 'Invalid sign in - try again'
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signin.html', context)

@login_required
def profile(request,username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            return redirect('profile', user_form.username)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)

        distros = Distro.objects.filter(user=user)
        patches = Patch.objects.filter(distro__user=user)
        return render(request, 'users/profile.html', context={'form': form, 'user': user, 'distros': distros, 'patches': patches})

    return redirect("profile")

def contact(request):
    return render(request, 'contact.html')