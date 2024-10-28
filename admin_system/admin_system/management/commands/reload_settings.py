from django.core.management.base import BaseCommand
import os

from admin_system.admin_core.models import ProjectSetting


class Command(BaseCommand):
    help = 'Recharge les paramètres du projet depuis la base de données.'

    def handle(self, *args, **options):
        project_settings = ProjectSetting.objects.all()
        for setting in project_settings:
            os.environ[setting.key] = setting.value
        self.stdout.write(self.style.SUCCESS('Paramètres du projet rechargés avec succès.'))
