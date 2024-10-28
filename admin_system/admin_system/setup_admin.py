# setup_admin.py
from django.core.management import call_command
from django.contrib.auth.models import Group

def setup_admin():
    Group.objects.get_or_create(name='Administrateur')
    Group.objects.get_or_create(name='Utilisateur')
    # Créer un super utilisateur
    call_command('createsuperuser')

if __name__ == "__main__":
    setup_admin()
