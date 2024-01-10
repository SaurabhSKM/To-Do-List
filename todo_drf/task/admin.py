from django.contrib import admin
from .models import Task, Tag


# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "Due_date", "status")
    list_filter = ("status", "tag")
    search_fields = ("title", "description")
    date_hierarchy = "Due_date"

    fieldsets = (
        ("Task Details", {"fields": ("title", "description", "Due_date", "status")}),
        (
            "Tags",
            {
                "fields": ("tag",),
            },
        ),
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    search_fields = (
        "id",
        "title",
    )


admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)
