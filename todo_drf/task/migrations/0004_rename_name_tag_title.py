# Generated by Django 5.0 on 2023-12-26 08:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0003_tag_remove_task_completed_task_due_date_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tag",
            old_name="name",
            new_name="title",
        ),
    ]
