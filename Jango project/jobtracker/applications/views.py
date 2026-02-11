from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .models import JobApplication, TrackedCompany
from .forms import JobApplicationForm, TrackedCompanyForm, SignUpForm


# =========================
# USER SIGNUP (STEP 2)
# =========================
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


# =========================
# DASHBOARD (POINT 3)
# =========================
@login_required
def dashboard(request):
    jobs = JobApplication.objects.filter(user=request.user)
    companies = TrackedCompany.objects.filter(user=request.user)

    return render(
        request,
        'dashboard.html',
        {
            'jobs': jobs,
            'companies': companies
        }
    )


# =========================
# ADD COMPANY TO TRACK (POINT 4)
# =========================
@login_required
def add_company(request):
    if request.method == 'POST':
        form = TrackedCompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            return redirect('dashboard')
    else:
        form = TrackedCompanyForm()

    return render(request, 'add_company.html', {'form': form})