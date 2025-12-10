from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("client_ip", "amount", "created_at")
    list_filter = ("created_at",)
    search_fields = ("client_ip",)
    readonly_fields = ("id", "client_ip", "amount", "created_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.site_header = "Bob's Corn Shop Administration"
admin.site.site_title = "Bob's Corn Portal"
admin.site.index_title = "Bienvenido al Panel de Auditoría"
