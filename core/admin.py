from django.contrib import admin
from core.models import Category,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Address,Cart,CartItem,Variation,Payment,OrderCancellationReason,OrderCancellation,Coupon,Offer,Wallet,WalletTransaction

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

# class ProductItemAdmin(admin.TabularInline):
#     model = ProductItem
#     extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['title','user','product_image','category','product_status']


class VariationAdmin(admin.ModelAdmin):
    list_display = ['product','variation_category','variation_value','is_active']
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value','is_active')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category_image']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title','vendor_image']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','payment_id','payment_method','amount_paid','status','created_at']

    
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user','price','paid_status','order_date','product_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order','invoice_no','product','image','qty','price','total']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product','rating','review']

class WhishListAdmin(admin.ModelAdmin):
    list_display = ['user','product','date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','first_name','last_name']

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id']


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product','qty','is_active']

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code','discount','valid_from','valid_to','active']


class OfferAdmin(admin.ModelAdmin):
    list_display = ['name','off_percent','start_date','end_date']
# class CartAdmin(admin.ModelAdmin):
#     inlines = [CartItemAdmin]
#     list_display = ['cart','user','product','qty']


class WalletAdmin(admin.ModelAdmin):
    list_display = ['balance']

class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['amount','type','date']

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderItems,CartOrderItemsAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(WhishList,WhishListAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(OrderCancellationReason)
admin.site.register(OrderCancellation)
admin.site.register(Coupon,CouponAdmin)
admin.site.register(Offer,OfferAdmin)
admin.site.register(Wallet,WalletAdmin)
admin.site.register(WalletTransaction,WalletTransactionAdmin)


