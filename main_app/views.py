from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Distro, Patch
from main_app.models import Distro, Patch
from django.http import Http404
from .forms import PatchForm
from main_app.forms import UploadForm, PatchForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm


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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')