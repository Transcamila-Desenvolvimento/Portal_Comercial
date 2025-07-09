# usuarios/admin.py
from django.contrib import admin
from .models import Profile
from django.utils.safestring import mark_safe

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'foto_preview']
    readonly_fields = ['foto_preview']

    def foto_preview(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="100" />')
        return "Sem foto"
    foto_preview.short_description = "Pré-visualização"