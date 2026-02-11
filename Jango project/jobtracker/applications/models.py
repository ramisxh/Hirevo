from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    deadline = models.DateField()
    status = models.CharField(max_length=20)
    applied_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} - {self.role}"


class TrackedCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    career_url = models.URLField()

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class JobPosting(models.Model):
    tracked_company = models.ForeignKey(
        TrackedCompany, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
