from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'country', 'role', 'is_active')
    list_filter = ('role', 'country')
    search_fields = ('first_name', 'email', 'country')
    exclude = ('password',)
