from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Career, ContactMessage, Course, EntranceExam, Roadmap, Scholarship, Student, TeamMember


@override_settings(SECURE_SSL_REDIRECT=False)
class CareerPathTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create_user(
            username="student1",
            email="student@example.com",
            full_name="Test Student",
            class_name="MPC",
            phone_number="9876543210",
            password="StrongPass123!",
        )

        self.roadmap = Roadmap.objects.create(
            name="MPC",
            slug="mpc",
            description="A science stream for engineering and technical careers.",
            eligibility="Interested in mathematics and science.",
            duration="2 years",
            subjects="Mathematics, Physics, Chemistry",
            courses="Engineering and technical programs",
            entrance_exams="JEE Main, AP EAPCET",
            higher_education="Engineering, research, design",
            career_opportunities="Software, design, manufacturing",
            government_opportunities="Public engineering jobs",
            private_opportunities="IT and manufacturing roles",
            skills="Problem solving, reasoning, team work",
            future_scope="Strong career value in engineering and innovation.",
        )

        self.career = Career.objects.create(
            name="Engineering",
            slug="engineering",
            description="Engineering careers build technology and physical systems.",
            eligibility="Strong interest in mathematics and science.",
            education_required="B.E. or B.Tech",
            entrance_exams="JEE Main, AP EAPCET",
            skills="Problem solving, logic, design",
            higher_studies="M.Tech, PhD, specializations",
            jobs="Software engineer, design engineer, analyst",
            future_scope="Technology and infrastructure growth.",
        )

        self.course = Course.objects.create(
            name="B.Tech Computer Science",
            slug="btech-computer-science",
            description="Study of computing, software, and digital systems.",
            eligibility="MPC or equivalent with strong mathematics.",
            duration="4 years",
            stream="Engineering",
            entrance_exam="JEE Main, AP EAPCET",
            career_opportunities="Software roles, AI, data, product engineering",
            higher_studies="M.Tech, MS, AI, data science",
        )

        self.scholarship = Scholarship.objects.create(
            name="Post Matric Scholarship",
            slug="post-matric-scholarship",
            eligibility="Eligible students meeting institutional requirements.",
            education_level="School and college",
            category="General support",
            income_requirement="As per scheme rules",
            benefits="Fee support and maintenance allowance",
            application_process="Apply through the official portal with documentation.",
            official_website="https://example.com",
            state_or_central="Central",
            notes="Verify all details with the official notice.",
        )

        self.exam = EntranceExam.objects.create(
            name="JEE Main",
            slug="jee-main",
            full_form="Joint Entrance Examination Main",
            eligibility="Students completing 12th class with required subjects.",
            purpose="Engineering admissions",
            conducting_authority="NTA",
            courses="Engineering and technical programs",
            exam_pattern="Objective questions covering Physics, Chemistry, Mathematics.",
            application_process="Register online and complete the application process.",
            official_website="https://example.com",
            notes="Check official announcements for important dates.",
        )

        self.team_member = TeamMember.objects.create(
            name="Team Member 1",
            role="Academic Counselor",
            description="Helps students explore education and career pathways.",
            contact="CareerPath support channels",
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CareerPath")
        self.assertContains(response, "JOIN OUR CAREERPATH WHATSAPP GROUP")

    def test_student_registration(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "New Student",
                "email": "newstudent@example.com",
                "class_name": "BiPC",
                "phone_number": "9988776655",
                "password": "StrongPass123!",
                "confirm_password": "StrongPass123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        student = Student.objects.get(email="newstudent@example.com")
        self.assertTrue(student.check_password("StrongPass123!"))
        self.assertNotEqual(student.password, "StrongPass123!")

    def test_duplicate_registration_is_blocked(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "Duplicate Student",
                "email": "student@example.com",
                "class_name": "MEC",
                "phone_number": "9988776655",
                "password": "StrongPass123!",
                "confirm_password": "StrongPass123!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already registered")

    def test_student_login_logout(self):
        login_response = self.client.post(
            reverse("login"),
            {"email": "student@example.com", "password": "StrongPass123!"},
            follow=True,
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertContains(login_response, "Welcome back")
        self.assertTrue(login_response.wsgi_request.user.is_authenticated)

        logout_response = self.client.post(reverse("logout"), follow=True)
        self.assertEqual(logout_response.status_code, 200)
        self.assertFalse(logout_response.wsgi_request.user.is_authenticated)

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {"email": "student@example.com", "password": "incorrect"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password")

    def test_logout_rejects_get_requests(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 405)

    def test_registration_rejects_case_insensitive_duplicate_email(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "Duplicate Student",
                "email": "STUDENT@EXAMPLE.COM",
                "class_name": "MEC",
                "phone_number": "9988776655",
                "password": "StrongPass123!",
                "confirm_password": "StrongPass123!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already registered")
        self.assertEqual(Student.objects.filter(email__iexact="student@example.com").count(), 1)

    def test_registration_rejects_password_mismatch(self):
        response = self.client.post(
            reverse("register"),
            {
                "full_name": "Mismatch Student",
                "email": "mismatch@example.com",
                "class_name": "MPC",
                "phone_number": "9988776655",
                "password": "StrongPass123!",
                "confirm_password": "DifferentPass123!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match")
        self.assertFalse(Student.objects.filter(email="mismatch@example.com").exists())

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_page_for_logged_in_user(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, Test Student")

    def test_roadmap_pages(self):
        list_response = self.client.get(reverse("roadmap_list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "MPC")

        detail_response = self.client.get(reverse("roadmap_detail", args=[self.roadmap.slug]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Engineering and technical programs")
        filtered_response = self.client.get(reverse("roadmap_list"), {"pathway": "MPC"})
        self.assertEqual(filtered_response.status_code, 200)
        self.assertContains(filtered_response, self.roadmap.name)

    def test_invalid_roadmap_slug_returns_404(self):
        response = self.client.get(reverse("roadmap_detail", args=["not-a-roadmap"]))
        self.assertEqual(response.status_code, 404)

    def test_career_pages(self):
        list_response = self.client.get(reverse("career_list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "Engineering")

        detail_response = self.client.get(reverse("career_detail", args=[self.career.slug]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "B.E. or B.Tech")
        filtered_response = self.client.get(reverse("career_list"), {"career": self.career.name})
        self.assertEqual(filtered_response.status_code, 200)
        self.assertContains(filtered_response, self.career.name)

    def test_invalid_career_slug_returns_404(self):
        self.assertEqual(self.client.get(reverse("career_detail", args=["missing"])).status_code, 404)

    def test_course_pages(self):
        list_response = self.client.get(reverse("course_list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "B.Tech Computer Science")

        detail_response = self.client.get(reverse("course_detail", args=[self.course.slug]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Study of computing")
        self.assertContains(detail_response, "Software roles")
        filtered_response = self.client.get(reverse("course_list"), {"stream": "Engineering"})
        self.assertEqual(filtered_response.status_code, 200)
        self.assertContains(filtered_response, self.course.name)
        self.assertEqual(self.client.get(reverse("course_list"), {"stream": "invalid"}).status_code, 400)

    def test_invalid_course_slug_returns_404(self):
        self.assertEqual(self.client.get(reverse("course_detail", args=["missing"])).status_code, 404)

    def test_scholarship_pages(self):
        list_response = self.client.get(reverse("scholarship_list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "Post Matric Scholarship")

        detail_response = self.client.get(reverse("scholarship_detail", args=[self.scholarship.slug]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Fee support and maintenance allowance")
        filtered_response = self.client.get(reverse("scholarship_list"), {"category": "General support"})
        self.assertEqual(filtered_response.status_code, 200)
        self.assertContains(filtered_response, self.scholarship.name)

    def test_invalid_scholarship_slug_returns_404(self):
        self.assertEqual(self.client.get(reverse("scholarship_detail", args=["missing"])).status_code, 404)

    def test_exam_pages(self):
        list_response = self.client.get(reverse("exam_list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "JEE Main")

        detail_response = self.client.get(reverse("exam_detail", args=[self.exam.slug]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "Joint Entrance Examination Main")
        filtered_response = self.client.get(reverse("exam_list"), {"authority": "NTA"})
        self.assertEqual(filtered_response.status_code, 200)
        self.assertContains(filtered_response, self.exam.name)
        self.assertEqual(self.client.get(reverse("exam_list"), {"authority": "invalid"}).status_code, 400)

    def test_invalid_exam_slug_returns_404(self):
        self.assertEqual(self.client.get(reverse("exam_detail", args=["missing"])).status_code, 404)

    def test_ece_guidance_page(self):
        response = self.client.get(reverse("ece_guidance"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VLSI and semiconductor design")
        self.assertContains(response, "not admission guarantees")

    def test_team_page(self):
        response = self.client.get(reverse("team"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Team Member 1")
        self.assertContains(response, "JOIN OUR CAREERPATH WHATSAPP GROUP")
        self.assertContains(response, 'target="_blank" rel="noopener noreferrer"')

    def test_contact_page_sends_message(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Visitor",
                "email": "visitor@example.com",
                "subject": "Question",
                "message": "Hello CareerPath team!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(email="visitor@example.com").exists())

    def test_contact_page_rejects_invalid_email(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Visitor",
                "email": "not-an-email",
                "subject": "Question",
                "message": "Hello CareerPath team!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ContactMessage.objects.exists())

    def test_seed_command_is_repeatable_and_preserves_edited_content(self):
        self.roadmap.description = "Existing content edited in Admin."
        self.roadmap.save(update_fields=["description"])

        call_command("seed_data", stdout=StringIO())
        call_command("seed_data", stdout=StringIO())

        self.roadmap.refresh_from_db()
        self.assertEqual(self.roadmap.description, "Existing content edited in Admin.")
        self.assertEqual(TeamMember.objects.count(), 5)

    def test_contact_messages_requires_staff(self):
        response = self.client.get(reverse("contact_messages"))
        self.assertEqual(response.status_code, 302)

        self.student.is_staff = True
        self.student.save(update_fields=["is_staff"])
        self.client.force_login(self.student)
        staff_response = self.client.get(reverse("contact_messages"))
        self.assertEqual(staff_response.status_code, 200)

    def test_search_rejects_excessively_long_query(self):
        response = self.client.get(reverse("roadmap_list"), {"q": "x" * 101})
        self.assertEqual(response.status_code, 400)
