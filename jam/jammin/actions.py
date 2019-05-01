from .models import Account, EmployeeAccount

def hire(modeladmin, request, queryset):
	for query in queryset:
		email = query.name.lower() + query.surname.lower() + '@jammin.com'
		account = Account.objects.create_user(email, query.name, query.surname, 'ptisdaddy')
		account.is_employee = true
		employee.saved()
		employee = EmployeeAccount.objects.create_employee(account, query.name, query.surname)
		query.delete()