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

class DistroCreate(CreateView):
    model = Distro
    fields = '__all__'
    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

class DistroUpdate(UpdateView):
    model = Distro
    fields = ['website', 'description']

class DistroDelete(DeleteView):
    model = Distro
    success_url = '/distros/'

# def distro(request, distro_id):
#     distro = Distro.objects.get(pk=distro_id)
#     if distro is not None:
#         return render(request, 'distros/distro.html', {'distro': distro})
#     else:
#         raise Http404('Distro does not exist.')
    
# def patch(request, patch_id):
#     patch = Patch.objects.get(pk=patch_id)
#     if patch is not None:
#         return render(request, 'patches/patch.html', {'patch': patch})
#     else:
#         raise Http404('Patch does not exist.')
    
def patch_index(request):
    patches = Patch.objects.all()
    return render(request, 'patches/index.html', {'patches': patches})

def patch_detail(request, patch_id):
    patch = Patch.objects.get(id=patch_id)
    return render(request, 'patches/detail.html', {'patch': patch})

# def add_patch(request, distro_id):
#     form = PatchForm(request.POST)
#     if form.is_valid():
#         new_patch = form.save(commit=False)
#         new_patch.distro_id = distro_id
#         new_patch.save()
#     return redirect('distro-detail', distro_id=distro_id)

class PatchCreate(CreateView):
    model = Patch
    fields = '__all__'
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
            return redirect('distro_index')  # Redirect after successful save
    else:
        form = UploadForm()
    
    return render(request, 'main_app/distro_form.html', {'form': form})

def patch_upload(request):
    if request.method == 'POST':
        form = PatchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('patch_index')  # Redirect after successful save
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
            return redirect('distro_index')
        else:
            error_message = 'Invalid sign up - try again'
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
        # if form.is_valid():    
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            print(f"User is not none")
            return redirect('home')
    # else:
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
        # form.fields['description'].widget.attrs = {'rows': 1}

        distros = Distro.objects.filter(user=user)
        return render(request, 'users/profile.html', context={'form': form, 'user': user, 'distros': distros})

    return redirect("homepage")

def contact(request):
    return render(request, 'contact.html')