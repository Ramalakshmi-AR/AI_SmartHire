from django.db import models


class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    skills = models.TextField(blank=True, null=True)  # ✅ FIX
    experience = models.IntegerField()
    uploaded_file = models.FileField(upload_to='resumes/')
    screening_score = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=100)
    required_skills = models.TextField()
    min_experience = models.IntegerField()

    def __str__(self):
        return self.title




def match_jobs(skills, experience):
    matched_jobs = []
    jobs = Job.objects.all()

    for job in jobs:
        job_skills = job.required_skills.lower().split(',')
        if any(skill in job_skills for skill in skills):
            if experience >= job.min_experience:
                matched_jobs.append(job)

    return matched_jobs

class JobApplication(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resume.name} applied for {self.job.title}"

