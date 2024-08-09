from django.contrib import admin
from .models import *

admin.site.register(AuthUser)
admin.site.register(UserProfile)


from django.contrib import admin
from .models import AccountRecoveryRequest

@admin.register(AccountRecoveryRequest)
class AccountRecoveryRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'government_id', 'submitted_at', 'processed', 'approved')
    list_filter = ('processed', 'approved')
    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} requests have been approved.")
    approve_requests.short_description = "Approve selected recovery requests"


#i an going to eat when but i have completed all section when im back its to test it if its working and deploy
