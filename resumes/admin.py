# admin.py
from django.contrib import admin
from .models import Resume, Job
from .models import Resume, Job, JobApplication

admin.site.register(Resume)
admin.site.register(Job)
admin.site.register(JobApplication)
