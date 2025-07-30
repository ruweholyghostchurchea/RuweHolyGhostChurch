
from django.contrib import admin
from .models import Diocese, Pastorate, Church

@admin.register(Diocese)
class DioceseAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'bishop_name', 'is_active', 'created_at']
    list_filter = ['country', 'is_active', 'created_at']
    search_fields = ['name', 'bishop_name', 'country']
    ordering = ['country', 'name']

@admin.register(Pastorate)
class PastorateAdmin(admin.ModelAdmin):
    list_display = ['name', 'diocese', 'pastor_name', 'is_active', 'created_at']
    list_filter = ['diocese__country', 'diocese', 'is_active', 'created_at']
    search_fields = ['name', 'pastor_name', 'diocese__name']
    ordering = ['diocese', 'name']

@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ['name', 'pastorate', 'diocese_name', 'head_teacher_name', 'is_active', 'created_at']
    list_filter = ['pastorate__diocese__country', 'pastorate__diocese', 'pastorate', 'is_active', 'created_at']
    search_fields = ['name', 'head_teacher_name', 'pastorate__name', 'pastorate__diocese__name']
    ordering = ['pastorate__diocese', 'pastorate', 'name']
    
    def diocese_name(self, obj):
        return obj.pastorate.diocese.name
    diocese_name.short_description = 'Diocese'
    diocese_name.admin_order_field = 'pastorate__diocese__name'
