from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import User, Incident, Officer, GroupOfficer, PermissionOfficer

class OfficerAdmin(admin.ModelAdmin):
    list_display = ('username', 'officer_id', 'zip')  # Customize the fields displayed in the list view

    search_fields = ('username', 'officer_id')  # Enable searching by these fields

    list_filter = ('zip',)
    exclude = ["email"]
    def save_model(self, request, obj, form, change):
        # Hash the password before saving
        obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

admin.site.register(User)
admin.site.register(Incident)
admin.site.register(Officer, OfficerAdmin)
