from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactForm, LoginForm, StudentRegistrationForm
from .models import Career, ContactMessage, Course, EntranceExam, Roadmap, Scholarship, TeamMember


def _validated_filter(request, key, allowed_values=None):
    value = request.GET.get(key, "").strip()
    if len(value) > 100 or (allowed_values is not None and value and value not in allowed_values):
        return None, HttpResponseBadRequest("Invalid search or filter value.")
    return value, None


def home(request):
    roadmaps = Roadmap.objects.all()[:6]
    careers = Career.objects.all()[:6]
    courses = Course.objects.all()[:6]
    scholarships = Scholarship.objects.all()[:3]
    exams = EntranceExam.objects.all()[:4]
    return render(
        request,
        "home.html",
        {
            "roadmaps": roadmaps,
            "careers": careers,
            "courses": courses,
            "scholarships": scholarships,
            "exams": exams,
            "career_count": Career.objects.count(),
            "course_count": Course.objects.count(),
            "scholarship_count": Scholarship.objects.count(),
            "exam_count": EntranceExam.objects.count(),
        },
    )


def register_view(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please login to continue.")
            return redirect("login")
    else:
        form = StudentRegistrationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"].strip(),
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.full_name}!")
                return redirect("dashboard")
            messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


@login_required(login_url="login")
def dashboard(request):
    return render(request, "dashboard.html", {"student": request.user})


def roadmap_list(request):
    query, error = _validated_filter(request, "q")
    if error:
        return error
    pathways = list(Roadmap.objects.order_by().values_list("name", flat=True).distinct())
    pathway, error = _validated_filter(request, "pathway", pathways)
    if error:
        return error
    roadmaps = Roadmap.objects.all()
    if query:
        roadmaps = roadmaps.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if pathway:
        roadmaps = roadmaps.filter(name=pathway)
    return render(
        request,
        "roadmap_list.html",
        {"roadmaps": roadmaps, "query": query, "pathways": pathways, "selected_pathway": pathway},
    )


def roadmap_detail(request, slug):
    roadmap = get_object_or_404(Roadmap, slug=slug)
    return render(request, "roadmap_detail.html", {"roadmap": roadmap})


def career_list(request):
    query, error = _validated_filter(request, "q")
    if error:
        return error
    career_names = list(Career.objects.order_by().values_list("name", flat=True).distinct())
    career_name, error = _validated_filter(request, "career", career_names)
    if error:
        return error
    careers = Career.objects.all()
    if query:
        careers = careers.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(skills__icontains=query)
            | Q(education_required__icontains=query)
        )
    if career_name:
        careers = careers.filter(name=career_name)
    return render(
        request,
        "career_list.html",
        {"careers": careers, "query": query, "career_names": career_names, "selected_career": career_name},
    )


def career_detail(request, slug):
    career = get_object_or_404(Career, slug=slug)
    return render(request, "career_detail.html", {"career": career})


def course_list(request):
    query, error = _validated_filter(request, "q")
    if error:
        return error
    streams = list(Course.objects.order_by().values_list("stream", flat=True).distinct())
    stream, error = _validated_filter(request, "stream", streams)
    if error:
        return error
    courses = Course.objects.all()
    if query:
        courses = courses.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(stream__icontains=query)
            | Q(eligibility__icontains=query)
        )
    if stream:
        courses = courses.filter(stream=stream)
    return render(
        request,
        "course_list.html",
        {"courses": courses, "query": query, "streams": streams, "selected_stream": stream},
    )


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, "course_detail.html", {"course": course})


def scholarship_list(request):
    query, error = _validated_filter(request, "q")
    if error:
        return error
    categories = list(Scholarship.objects.order_by().values_list("category", flat=True).distinct())
    category, error = _validated_filter(request, "category", categories)
    if error:
        return error
    scholarships = Scholarship.objects.all()
    if query:
        scholarships = scholarships.filter(
            Q(name__icontains=query)
            | Q(category__icontains=query)
            | Q(eligibility__icontains=query)
            | Q(education_level__icontains=query)
        )
    if category:
        scholarships = scholarships.filter(category=category)
    return render(
        request,
        "scholarship_list.html",
        {
            "scholarships": scholarships,
            "query": query,
            "categories": categories,
            "selected_category": category,
        },
    )


def scholarship_detail(request, slug):
    scholarship = get_object_or_404(Scholarship, slug=slug)
    return render(request, "scholarship_detail.html", {"scholarship": scholarship})


def exam_list(request):
    query, error = _validated_filter(request, "q")
    if error:
        return error
    authorities = list(EntranceExam.objects.order_by().values_list("conducting_authority", flat=True).distinct())
    authority, error = _validated_filter(request, "authority", authorities)
    if error:
        return error
    exams = EntranceExam.objects.all()
    if query:
        exams = exams.filter(
            Q(name__icontains=query)
            | Q(full_form__icontains=query)
            | Q(purpose__icontains=query)
            | Q(courses__icontains=query)
        )
    if authority:
        exams = exams.filter(conducting_authority=authority)
    return render(
        request,
        "exam_list.html",
        {"exams": exams, "query": query, "authorities": authorities, "selected_authority": authority},
    )


def exam_detail(request, slug):
    exam = get_object_or_404(EntranceExam, slug=slug)
    return render(request, "exam_detail.html", {"exam": exam})


def ece_guidance(request):
    return render(request, "ece_guidance.html")


def team(request):
    members = TeamMember.objects.order_by("id")[:5]
    return render(request, "team.html", {"members": members})


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully. We will get back to you soon.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


@staff_member_required
def contact_messages(request):
    messages_list = ContactMessage.objects.all()[:20]
    return render(request, "admin_contact_messages.html", {"messages": messages_list})
