from django.shortcuts import redirect, render
from .models import Job
from .form import ApplyForm, JobForm
from .filters import JobFilter
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.


def job_list(request):
    job_list = Job.objects.all()

    # # filters
    myfilter = JobFilter(request.GET, job_list)
    job_list = myfilter.qs

    paginator = Paginator(job_list, 6)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"jobs": page_obj, "myfilter": myfilter}
    return render(request, "job/job_list.html", context)


def job_detail(request, slug):
    job_detail = Job.objects.get(slug=slug)

    if request.method == "POST":
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.job = job_detail
            myform.save()
    else:
        form = ApplyForm()

    context = {
        "job": job_detail,
        "form_job": form,
    }
    return render(request, "job/job_detail.html", context)


@login_required
def add_job(request):
    if request.method == "POST":
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()
            return redirect(reverse("jobs:job_list"))
    else:
        form = JobForm()

    context = {
        "form": form,
    }
    return render(request, "job/add_job.html", context)
