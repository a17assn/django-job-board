from django.shortcuts import redirect, render
from .form import SignupForm, UserForm, ProfileForm
from django.contrib.auth import authenticate, login
from .models import Profile
from django.urls import reverse
from django.contrib import messages

# Create your views here.


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/accounts/profile")
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})


def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile})


def profile_edit(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        userform = UserForm(request.POST, instance=request.user)
        profileform = ProfileForm(request.POST, request.FILES, instance=profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            myprofile = profileform.save(commit=False)
            myprofile.user = request.user
            myprofile.save()
            return redirect(reverse("accounts:profile"))

    else:
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/profile_edit.html",
        {"userform": userform, "profileform": profileform},
    )


# def my_reservation(request):
#     user_reservation = PropertyBook.objects.filter(name=request.user)
#     return render(
#         request, "profile/my_reservation.html", {"user_reservation": user_reservation}
#     )


# def add_feedback(request, slug):
#     property = get_object_or_404(Property, slug=slug)

#     try:
#         user_feedback = get_object_or_404(
#             PropertyReview, property=property, author=request.user
#         )
#         if request.method == "POST":
#             form = PropertyReviewForm(request.POST, instance=user_feedback)
#             if form.is_valid():
#                 form.save()

#         else:
#             form = PropertyReviewForm(instance=user_feedback)
#         return render(
#             request,
#             "profile/property_feedback.html",
#             {"form": form, "property": property},
#         )

#     except:
#         if request.method == "POST":
#             form = PropertyReviewForm(request.POST)
#             if form.is_valid():
#                 myform = form.save(commit=False)
#                 myform.property = property
#                 myform.author = request.user
#                 myform.save()

#         else:
#             form = PropertyReviewForm()
#         return render(
#             request,
#             "profile/property_feedback.html",
#             {"form": form, "property": property},
#         )
