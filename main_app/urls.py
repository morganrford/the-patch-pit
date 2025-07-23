from django.urls import path, include
from . import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('distros/', views.distro_index, name='distro_index'),
    path('distros/<int:distro_id>/', views.distro_detail, name='distro_detail'),
    path('distros/create/', views.DistroCreate.as_view(), name='distro_create'),
    path('distros/<int:pk>/update/', views.DistroUpdate.as_view(), name='distro_update'),
    path('distros/<int:pk>/delete/', views.DistroDelete.as_view(), name='distro_delete'),
    # path('distros/<int:distro_id>', views.distro),
    # path('patches/<int:patch_id>', views.patch),    
    path('patches/', views.patch_index, name='patch_index'),
    # path('distros/<int:distro_id>/add-patch/', views.add_patch, name='add-patch'),
    path('patches/create/', views.PatchCreate.as_view(), name='patch_create'),
    path('patches/<int:pk>/update/', views.PatchUpdate.as_view(), name='patch_update'),
    path('patches/<int:pk>/delete/', views.PatchDelete.as_view(), name='patch_delete'),
    path('distros/upload', views.distro_upload, name='distro_upload'),
    path('patches/upload', views.patch_upload, name='patch_upload'),
    path('patches/<int:patch_id>/', views.patch_detail, name='patch_detail'),
    path('accounts/signup/', views.signup, name='signup'),
    # path('accounts/signin/', views.signin, name='signin'),
    path('accounts/logout/', views.logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)