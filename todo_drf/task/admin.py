from django.contrib import admin
from .models import Task, Tag
from django.core.exceptions import ValidationError
from datetime import timezone
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'Due_date', 'status')
    list_filter = ('status', 'tag')
    search_fields = ('title', 'description')
    date_hierarchy = 'Due_date'

    fieldsets = (
        ('Task Details', {
            'fields': ('title', 'description', 'Due_date', 'status')
        }),
        ('Tags', {
            'fields': ('tag',),
        }),
    )

    def save_model(self, request, obj, form, change):
        # Enforce validation checks before saving the model
        if obj.Due_date and obj.Due_date < timezone.now().date():
            raise ValidationError("Due date cannot be in the past.")
        super().save_model(request, obj, form, change)

class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)  

admin.site.register(Task, TaskAdmin)
admin.site.register(Tag, TagAdmin)
