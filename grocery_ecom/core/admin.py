from django.contrib import admin
from core.models import Category,Vendor,Tags,Brand,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address,Cart,CartItem,ProductItem

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

# class ProductItemAdmin(admin.TabularInline):
#     model = ProductItem
#     extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user','title','product_image','category','product_status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category_image']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title','vendor_image']

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

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product','qty']

# class CartAdmin(admin.ModelAdmin):
#     inlines = [CartItemAdmin]
#     list_display = ['cart','user','product','qty']

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderItems,CartOrderItemsAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(WhishList,WhishListAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(CartItem,CartItemAdmin)

