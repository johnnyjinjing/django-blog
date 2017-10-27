from django.db import models, migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.management import create_permissions

def add_group_permissions(apps, schema_editor):

    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    # reader
    group, created = Group.objects.get_or_create(name='reader')

    # writer
    group, created = Group.objects.get_or_create(name='writer')
    if created:
        permission_writer = ['add_category', 'add_tag', 'add_post',
            'change_post', 'delete_post']

        for codename in permission_writer:
            permission = Permission.objects.get(codename=codename)
            group.permissions.add(permission)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions),
    ]