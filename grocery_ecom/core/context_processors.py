from core.models import Category,Vendor,Tags,Brand,Product,ProductImages,CartOrder,CartOrderItems,ProductReview,WhishList,Countrty,State,City,Address

def default(request):
    categories = Category.objects.all()
    return {
        'categories':categories
    }