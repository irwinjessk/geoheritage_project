from django.contrib import admin
from .models import Patrimoine


@admin.register(Patrimoine)
class PatrimoineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'ville', 'created_by', 'created_at')
    list_filter = ('type', 'ville', 'created_at')
    search_fields = ('nom', 'description', 'ville')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
