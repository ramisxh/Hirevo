from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail

from .models import (
    JobApplication,
    TrackedCompany,
    JobPosting
)
from .scraper import fetch_jobs


# =====================================
# POINT 3 – DEADLINE REMINDER TASK
# =====================================
@shared_task
def deadline_reminder():
    tomorrow = now().date() + timedelta(days=1)

    applications = JobApplication.objects.filter(deadline=tomorrow)

    for app in applications:
        if app.user.email:
            send_mail(
                "Deadline Reminder",
                f"Deadline tomorrow for {app.role} at {app.company.name}",
                "noreply@app.com",
                [app.user.email],
            )


# =====================================
# POINT 4 – NEW JOB ALERT TASK
# =====================================
@shared_task
def check_new_jobs():
    companies = TrackedCompany.objects.all()

    for company in companies:
        jobs = fetch_jobs(company.career_url)

        for job_title in jobs:
            exists = JobPosting.objects.filter(
                tracked_company=company,
                title=job_title
            ).exists()

            if not exists:
                JobPosting.objects.create(
                    tracked_company=company,
                    title=job_title
                )

                if company.user.email:
                    send_mail(
                        "New Job Alert",
                        f"New job opening at {company.name}: {job_title}",
                        "noreply@app.com",
                        [company.user.email],
                    )
