from django.shortcuts import render, redirect
from .models import Resume, Job
from .forms import ResumeForm
from PyPDF2 import PdfReader
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Resume, JobApplication

# Simple AI logic for screening and job matching
def calculate_screening_score(resume):
    # Example: 1 point for each skill matched to a predefined skill list
    skills_required = ["Python", "Django", "Machine Learning", "AI", "React"]
    score = 0
    for skill in skills_required:
        if skill.lower() in resume.skills.lower():
            score += 20
    # Experience bonus
    score += min(resume.experience * 5, 20)
    return min(score, 100)

def match_jobs(skills, experience):
    matched_jobs = []
    jobs = Job.objects.all()

    # normalize resume skills
    resume_skills = [skill.strip().lower() for skill in skills]

    for job in jobs:
        job_skills = [s.strip().lower() for s in job.required_skills.split(',')]

        # check skill match
        skill_match = set(resume_skills) & set(job_skills)

        # check experience match
        if skill_match and experience >= job.min_experience:
            matched_jobs.append(job)

    return matched_jobs


def upload_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            resume = form.save(commit=False)

            # 1. Read PDF
            pdf_text = extract_text_from_pdf(resume.uploaded_file)

            # 2. Extract skills
            skills = extract_skills(pdf_text)

            # 3. Calculate score
            resume.screening_score = calculate_score(skills, resume.experience)

            # 4. Save extracted skills
            resume.skills = ", ".join(skills)
            resume.save()

            # 5. Match jobs
            jobs = match_jobs(skills, resume.experience)

            # 6. SEND DATA TO TEMPLATE
            return render(request, 'resumes/recommendations.html', {
                'resume': resume,
                'skills': skills,
                'jobs': jobs
            })
    else:
        form = ResumeForm()

    return render(request, 'resumes/upload.html', {'form': form})




def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

SKILL_SET = [
    "python", "django", "machine learning", "ai",
    "data science", "sql", "react", "html", "css", "javascript"
]

def extract_skills(text):
    found = []
    for skill in SKILL_SET:
        if skill in text:
            found.append(skill)
    return found


def calculate_score(skills, experience):
    score = len(skills) * 10
    score += min(experience * 5, 20)
    return min(score, 100)

def apply_job(request, resume_id, job_id):
    resume = get_object_or_404(Resume, id=resume_id)
    job = get_object_or_404(Job, id=job_id)

    # Save application
    JobApplication.objects.create(
        resume=resume,
        job=job
    )

    return render(request, 'resumes/apply_success.html', {
        'resume': resume,
        'job': job
    })

