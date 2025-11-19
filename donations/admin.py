from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from .models import DonationMoney, DonationGoods

@admin.register(DonationMoney)
class DonationMoneyAdmin(admin.ModelAdmin):
    list_display = ("id", "display_donor", "amount_display", "crisis_post", "payment_method", "donated_at")
    list_filter = ("payment_method", "is_anonymous", "donated_at", "crisis_post")
    search_fields = ("donor__username", "donor_name", "donor_email", "transaction_id", "crisis_post__title")
    readonly_fields = ("donated_at",)
    ordering = ("-donated_at",)
    
    def display_donor(self, obj):
        if obj.is_anonymous:
            return format_html('<i style="color: gray;">Anonymous</i>')
        return obj.display_name
    display_donor.short_description = "Donor"
    
    def amount_display(self, obj):
        return format_html('<b style="color: green;">৳ {}</b>', obj.amount)
    amount_display.short_description = "Amount (BDT)"
    amount_display.admin_order_field = "amount"
    
    # Show total donations in changelist
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        total = DonationMoney.objects.aggregate(total=Sum('amount'))['total'] or 0
        extra_context['total_donations'] = f"৳ {total:,.2f}"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(DonationGoods)
class DonationGoodsAdmin(admin.ModelAdmin):
    list_display = ("id", "display_donor", "item_description_short", "crisis_post", "quantity", "donated_at")
    list_filter = ("is_anonymous", "donated_at", "crisis_post")
    search_fields = ("donor__username", "donor_name", "item_description", "crisis_post__title")
    readonly_fields = ("donated_at",)
    ordering = ("-donated_at",)
    
    def display_donor(self, obj):
        if obj.is_anonymous:
            return format_html('<i style="color: gray;">Anonymous</i>')
        return obj.display_name
    display_donor.short_description = "Donor"
    
    def item_description_short(self, obj):
        return obj.item_description[:50] + "..." if len(obj.item_description) > 50 else obj.item_description
    item_description_short.short_description = "Items"