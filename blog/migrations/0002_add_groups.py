from django.db import models, migrations
from django.contrib.auth.models import Group

def add_group_permissions(apps, schema_editor):
    # reader
    group, created = Group.objects.get_or_create(name='reader')

    # writer
    group, created = Group.objects.get_or_create(name='writer')
    if created:
        group.permissions.add(
            [
                can_add_category,
                can_add_tag,
                can_add_post,
                can_change_post,
                can_delete_post,
            ])

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions),
    ]