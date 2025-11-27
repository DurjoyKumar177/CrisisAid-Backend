from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Simple redirect view
# def home_redirect(request):
#     return redirect('http://localhost:5173')

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Home redirect for social login
    # path("", home_redirect, name="home"),

    # Authentication
    path("api/accounts/auth/", include("dj_rest_auth.urls")),
    path("api/accounts/auth/signup/", include("dj_rest_auth.registration.urls")),
    path("accounts/", include("allauth.urls")),
    path("api/accounts/", include("accounts.urls")),
    
    # Crisis Management
    path("api/crisis/", include("crisis.urls")),
    
    # Donations
    path("api/donations/", include("donations.urls")),
    
    # Volunteers
    path("api/volunteers/", include("volunteers.urls")),
    
    # Updates & Comments
    path("api/updates/", include("updates.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)