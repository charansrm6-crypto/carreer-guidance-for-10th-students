from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("roadmaps/", views.roadmap_list, name="roadmap_list"),
    path("roadmap/<slug:slug>/", views.roadmap_detail, name="roadmap_detail"),
    path("careers/", views.career_list, name="career_list"),
    path("career/<slug:slug>/", views.career_detail, name="career_detail"),
    path("courses/", views.course_list, name="course_list"),
    path("course/<slug:slug>/", views.course_detail, name="course_detail"),
    path("scholarships/", views.scholarship_list, name="scholarship_list"),
    path("scholarship/<slug:slug>/", views.scholarship_detail, name="scholarship_detail"),
    path("exams/", views.exam_list, name="exam_list"),
    path("exam/<slug:slug>/", views.exam_detail, name="exam_detail"),
    path("ece-guidance/", views.ece_guidance, name="ece_guidance"),
    path("team/", views.team, name="team"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("admin-messages/", views.contact_messages, name="contact_messages"),
]
