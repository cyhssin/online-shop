from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
	list_display = ["email", "is_admin"]
	list_filter = ["is_admin"]
	readonly_fields = ["last_login"]

	fieldsets = (
		("Main", {"fields":("email", "sur_name", "for_name", "password")}),
		("Permissions", {"fields":("is_active", "is_admin", "is_superuser", "last_login", "groups", "user_permissions")}),
	)

	add_fieldsets = (
		(None, {"fields":("email", "sur_name", "for_name", "password1", "password2")}),
	)

	search_fields = ["email", "sur_name", "for_name"]
	ordering = ["for_name"]
	filter_horizontal = ["groups", "user_permissions"]

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		is_superuser = request.user.is_superuser
		if not is_superuser:
			form.base_fields["is_superuser"].disabled = True
		return form
