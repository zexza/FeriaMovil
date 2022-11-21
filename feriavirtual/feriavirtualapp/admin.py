from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import FormRegistroUsuario


class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('rol','imagen'),
        }),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rol','imagen')}),
    )
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Producto)

admin.site.register(Contrato)
admin.site.register(Transporte)