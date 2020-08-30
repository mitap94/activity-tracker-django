from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from core import models

class UserAdmin(BaseUserAdmin):
    
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'gender', 'profile_picture')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


# user
admin.site.register(models.User, UserAdmin)

# meal
admin.site.register(models.BaseFood)
admin.site.register(models.FoodAmount)
admin.site.register(models.Recipe)
admin.site.register(models.Meal)
admin.site.register(models.DailyMeal)

# measurement
admin.site.register(models.UserGoal)
admin.site.register(models.Measurement)