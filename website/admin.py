from django import forms
from django.contrib import admin

from .models import Career, ContactMessage, Course, EntranceExam, Roadmap, Scholarship, Student, TeamMember


class StudentAdminForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank to keep the current password. The value is stored using Django password hashing.",
    )

    class Meta:
        model = Student
        fields = "__all__"

    def save(self, commit=True):
        current_password = self.instance.password if self.instance.pk else None
        student = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            student.set_password(password)
        elif current_password:
            student.password = current_password
        elif not student.pk:
            student.set_unusable_password()
        if commit:
            student.save()
            self.save_m2m()
        return student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    fields = (
        "email",
        "username",
        "full_name",
        "class_name",
        "phone_number",
        "password",
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
        "user_permissions",
    )
    list_display = ("full_name", "email", "class_name", "phone_number", "is_active")
    search_fields = ("full_name", "email", "phone_number")
    list_filter = ("class_name", "is_active")
    ordering = ("full_name",)
    filter_horizontal = ("groups", "user_permissions")


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ("name", "duration", "created_at")
    search_fields = ("name", "description")
    list_filter = ("duration",)
    ordering = ("name",)


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ("name", "education_required", "future_scope")
    search_fields = ("name", "skills")
    list_filter = ("name",)
    ordering = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "duration", "stream")
    search_fields = ("name", "description", "stream")
    list_filter = ("stream",)
    ordering = ("name",)


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ("name", "education_level", "state_or_central")
    search_fields = ("name", "category", "eligibility")
    list_filter = ("state_or_central", "category")
    ordering = ("name",)


@admin.register(EntranceExam)
class EntranceExamAdmin(admin.ModelAdmin):
    list_display = ("name", "full_form", "conducting_authority")
    search_fields = ("name", "full_form", "courses")
    list_filter = ("conducting_authority",)
    ordering = ("name",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "contact")
    search_fields = ("name", "role")
    list_filter = ("role",)
    ordering = ("id",)

    def has_add_permission(self, request):
        return super().has_add_permission(request) and TeamMember.objects.count() < 5


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
