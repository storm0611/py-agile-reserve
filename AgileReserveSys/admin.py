from django.contrib import admin
from django.contrib.auth.admin import (
    UserAdmin
)

# Register your models here.
from .models import (
    CustomUser,
    Subscriber,
    MachineList
)

class CustomUserAdmin(admin.ModelAdmin):
    
    model = CustomUser
    list_display = ('username', 'email', 'verified_at', 'deactivated_at', 'is_first', 'can_book_num')
    # list_display = ["username", "verified_at", "deactivated_at", "is_first", "can_book_num"]

class SubscriberAdmin(admin.ModelAdmin):
    
    model = Subscriber
    list_display = ["email", "is_active", "created_at", "updated_at"]

class MachineListAdmin(admin.ModelAdmin):
    
    model = MachineList
    list_display = ["device_name", "fw_version", "serial_no", "device_host_name", "ip_address", "identification", "options", "user", "book_date"]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(MachineList, MachineListAdmin)