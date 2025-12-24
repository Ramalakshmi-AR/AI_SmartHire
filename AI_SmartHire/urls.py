from django.contrib import admin
from django.urls import path, include
from resumes.views import upload_resume

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upload_resume, name='home'),   # 👈 ADD THIS
    path('resumes/', include('resumes.urls')),
]
