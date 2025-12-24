from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('apply/<int:resume_id>/<int:job_id>/', views.apply_job, name='apply_job'),
]
