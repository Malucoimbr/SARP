import requests
from django.core.management.base import BaseCommand
from repositories.models import Repository

class Command(BaseCommand):
    help = 'Import assessment data from API'

    def handle(self, *args, **kwargs):
        # Simulando integração com o script de assessment
        assessment_data = [
            {
                "name": "Repo1",
                "project_id": 12345,
                "variables_protected": True,
                "runners_secure": False,
            },
            {
                "name": "Repo2",
                "project_id": 67890,
                "variables_protected": True,
                "runners_secure": True,
            },
        ]

        for repo in assessment_data:
            Repository.objects.update_or_create(
                project_id=repo["project_id"],
                defaults={
                    "name": repo["name"],
                    "variables_protected": repo["variables_protected"],
                    "runners_secure": repo["runners_secure"],
                    "status": 'approved' if repo["variables_protected"] and repo["runners_secure"] else 'rejected',
                },
            )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

