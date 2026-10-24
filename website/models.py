from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class Student(AbstractUser):
    CLASS_CHOICES = [
        ("10th", "10th"),
        ("MPC", "MPC"),
        ("BiPC", "BiPC"),
        ("MEC", "MEC"),
        ("CEC", "CEC"),
        ("Diploma", "Diploma"),
        ("ITI", "ITI"),
        ("Vocational", "Vocational"),
        ("Arts", "Arts"),
        ("Science", "Science"),
        ("Commerce", "Commerce"),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    class_name = models.CharField(max_length=50, choices=CLASS_CHOICES, default="10th")
    phone_number = models.CharField(max_length=15)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name", "class_name", "phone_number"]

    def clean(self):
        super().clean()
        self.email = self.email.strip().lower()
        if Student.objects.filter(email__iexact=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({"email": "A student account with this email already exists."})

    def save(self, *args, **kwargs):
        self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.email


class Roadmap(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    eligibility = models.TextField()
    duration = models.CharField(max_length=120)
    subjects = models.TextField()
    courses = models.TextField()
    entrance_exams = models.TextField()
    higher_education = models.TextField()
    career_opportunities = models.TextField()
    government_opportunities = models.TextField()
    private_opportunities = models.TextField()
    skills = models.TextField()
    future_scope = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Career(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    eligibility = models.TextField()
    education_required = models.TextField()
    entrance_exams = models.TextField()
    skills = models.TextField()
    higher_studies = models.TextField()
    jobs = models.TextField()
    future_scope = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default="")
    eligibility = models.TextField()
    duration = models.CharField(max_length=120)
    stream = models.CharField(max_length=80)
    entrance_exam = models.TextField()
    career_opportunities = models.TextField()
    higher_studies = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Scholarship(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    eligibility = models.TextField()
    education_level = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    income_requirement = models.CharField(max_length=200, blank=True)
    benefits = models.TextField()
    application_process = models.TextField()
    official_website = models.URLField(blank=True)
    state_or_central = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class EntranceExam(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    full_form = models.CharField(max_length=200)
    eligibility = models.TextField()
    purpose = models.TextField()
    conducting_authority = models.CharField(max_length=200)
    courses = models.TextField()
    exam_pattern = models.TextField()
    application_process = models.TextField()
    official_website = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    description = models.TextField()
    photo = models.ImageField(upload_to="team_photos/", blank=True, null=True)
    contact = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"
