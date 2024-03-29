# Generated by Django 5.0 on 2023-12-28 06:18

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=50, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("title", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=1000)),
                ("Due_date", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("OPEN", "Open"),
                            ("WORKING", "Working"),
                            ("DONE", "Done"),
                            ("OVERDUE", "Overdue"),
                        ],
                        default="OPEN",
                        max_length=10,
                    ),
                ),
                ("tag", models.ManyToManyField(blank=True, to="task.tag")),
            ],
        ),
    ]
