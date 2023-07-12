from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe
from userauths.models import User
from django.core.validators import FileExtensionValidator
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.functions import Lower


STATUS_CHOCE = (
    ("proccess", "Processing"),
    ("shipped", "Shipped"),
    ("deliverd", "Delivered"),
)
ADDRESS_TYPES = (
    ("home", "Home"),
    ("office", "Office")
)
PAYMENT_CHOiCE = (
    ("cod", "Cod"),
    ("online", "Online")
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published")
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20,prefix="cat", alphabet="abcdefghi123456789")
    title = models.CharField(max_length=100, default=None)
    image = models.FileField(upload_to="category",default='category-icon.png',validators=[FileExtensionValidator(['jpg', 'png','webp','jpeg', 'svg'])])
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True,null=True)
    

    class Meta:
        verbose_name_plural = "Categories"
        # constraints = [
        #     models.UniqueConstraint(
        #         Lower('title'),
        #         name='title_unique'
        #     ),
        # ]

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20,
                         prefix="ven", alphabet="abcdefghi123456789")
    title = models.CharField(max_length=100, default=None)
    image = models.ImageField(
        upload_to=user_directory_path, default='vendor-icon.png')
    # description = models.TextField(null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, default=None)
    contact = models.CharField(max_length=100, default=None)
    chat_resp_time = models.CharField(max_length=100, default=100)
    shipping_on_time = models.CharField(max_length=100, default=100)
    authentic_rating = models.CharField(max_length=100, default=10)
    days_return = models.CharField(max_length=10, default=10)
    warrenty_period = models.CharField(max_length=100, default=None)

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Tags(models.Model):
    pass


class Brand(models.Model):
    bid = ShortUUIDField(unique=True, length=10, max_length=20)
    title = models.CharField(max_length=100, default=None)
    image = models.ImageField(upload_to="brand", default='brand-icon.png')

    class Meta:
        verbose_name_plural = "Brand"

    def brand_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20)
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,related_name="category")
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100, default=None)
    image = models.ImageField(upload_to=user_directory_path, default='product-icon.png')
    # description = models.TextField(null=True, default=None,blank = True)
    description = RichTextUploadingField(null=True, default=None,blank = True)

    price = models.DecimalField(max_digits=100, decimal_places=2, default=None)
    discount_price = models.DecimalField(max_digits=100, decimal_places=2, default=None)
    stock_count = models.IntegerField(default=10)
    mfd = models.DateField(null = True,auto_now_add=False,blank=True)
    life = models.CharField(max_length=50,default=50)
    status = models.BooleanField(default=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=5, max_length=10,prefix="sku", alphabet="123456789")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False) 

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = (self.discount_price / self.price) * 100
        return new_price - 100


class ProductImages(models.Model):
    image = models.ImageField(
        upload_to='product-images', default="product.jpg")
    product = models.ForeignKey(Product,related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"

########################  Cart, Orderitems and Address  #######################


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Cart"

class CartItem(models.Model):
    # cart = models.ForeignKey(Cart,related_name="cart_items",on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty     = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Cart Items"

    def sub_total(self):
        return self.product.discount_price * self.qty
    
    def __str__(self):
        return self.product




class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderno = ShortUUIDField(unique=True, length=10,
                             max_length=20, prefix="od", alphabet="1234567890")
    price = models.DecimalField(
        max_digits=100, decimal_places=2, default=None)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(
        choices=STATUS_CHOCE, max_length=30, default="processing")
    
    payment_type = models.CharField(
        choices=PAYMENT_CHOiCE, max_length=30, default="cod")

    class Meta:
        verbose_name_plural = "Cart Order"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder,related_name="order_items",on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(
        choices=STATUS_CHOCE, max_length=30, default="processing")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(
        max_digits=100, decimal_places=2, default=None)
    total = models.DecimalField(
        max_digits=100, decimal_places=2, default=None)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

########################  Product Review  #######################


class ProductReview(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField(default=None)
    rating = models.CharField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating


class WhishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "wishlists"

    def __str__(self):
        return self.product.title


class Countrty(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Countrty, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "States"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    line1 = models.TextField(default=None,null=True,blank=True)
    pincode = models.CharField(max_length=6,null=True,blank=True)
    mobile = models.CharField(max_length=20, default=None,null=True,blank=True)
    type = models.CharField(choices=ADDRESS_TYPES, max_length=10, default="home")
    is_default = models.BooleanField(default=False,null=True,blank=True)
    # date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.first_name


class OrderAddress(models.Model):
    order = models.ForeignKey(CartOrder,related_name="order_address",on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    line1 = models.TextField(default=None,null=True,blank=True)
    pincode = models.CharField(max_length=6,null=True,blank=True)
    mobile = models.CharField(max_length=20, default=None,null=True,blank=True)
    type = models.CharField(choices=ADDRESS_TYPES, max_length=10, default="home")
    
    class Meta:
        verbose_name_plural = "Order Addresses"

    def __str__(self):
        return self.first_name

