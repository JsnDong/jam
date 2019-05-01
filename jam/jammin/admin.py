from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AccountCreationForm, AccountChangeForm
from .models import Account

class AccountAdmin(UserAdmin):
	form = AccountChangeForm
	add_form = AccountCreationForm

	list_display = ('email', 'name', 'surname', 'is_admin', 'is_employee', 'is_active')
	list_filter = ('is_admin', 'is_employee', 'is_active')
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal Details', {'fields': ('name', 'surname', 'dob')}),
		('Permissions', {'fields': ('is_admin', 'is_employee', 'is_active')}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'name', 'surname', 'dob', 'password1', 'password2')}
		),
	)

	search_fields = ('email', 'name', 'surname', 'dob')
	ordering = ('email',)
	filter_horizontal = ()

admin.site.register(Account, AccountAdmin)