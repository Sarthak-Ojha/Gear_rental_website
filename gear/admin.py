from django.contrib import admin
from django.core.mail import send_mail
from django.utils.html import format_html
from .models import Category, Product, Cart, CartItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_per_day', 'available', 'created_at']
    list_filter = ['category', 'available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['available', 'price_per_day']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'delivery_method', 'status', 'created_at', 'id_proof_link']
    list_filter = ['status', 'delivery_method', 'created_at']
    search_fields = ['user__username', 'user__email']
    list_editable = ['status']
    inlines = [OrderItemInline]

    def id_proof_link(self, obj):
        if obj.id_proof:
            return format_html("<a href='{}' target='_blank'>View ID</a>", obj.id_proof.url)
        return "No ID"
    id_proof_link.short_description = "ID Proof"

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Order.objects.get(pk=obj.pk)
            if old_obj.status != obj.status and obj.status.lower() == "confirmed":
                self.send_confirmation_email(obj)
        super().save_model(request, obj, form, change)

    def send_confirmation_email(self, order):
        user_email = order.user.email
        if not user_email:
            return

        subject = "Adventure Gear - Order Confirmed!"
        message = (
            f"Hi {order.user.first_name or order.user.username},\n\n"
            f"Your order #{order.id} has been confirmed.\n"
            f"Total: Rs. {order.total_amount}\n"
            f"Delivery Method: {order.delivery_method}\n\n"
            "Thank you for choosing Adventure Gear!"
        )

        send_mail(
            subject,
            message,
            None,  # Uses DEFAULT_FROM_EMAIL from settings
            [user_email],
            fail_silently=False,
        )
