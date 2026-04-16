from django.test import TestCase
from .models import Project

class ProjectModelTest(TestCase):
    def Test_create_project(self):
        project = Project.objects.create(
            title = "Education Drive",
            description = "Helping children",
            location = "Lucknow"
        )
        self.assertEqual(project.title,"Education Drive")
