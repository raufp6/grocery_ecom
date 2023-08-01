from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe
from userauths.models import User
from django.core.validators import FileExtensionValidator
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.functions import Lower
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError


STATUS_CHOCE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("deliverd", "Delivered"),
    ("canceled", "Canceled"),
    ("returned", "Returned"),
    ("completed", "Completed"),
)
ADDRESS_TYPES = (
    ("home", "Home"),
    ("office", "Office")
)
PAYMENT_CHOiCE = (
    ("cod", "Cod"),
    ("online", "Online")
)

VARIENT_CHOiCE = (
    ("text", "Text"),
    ("color", "Color"),
    ("image", "Image"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published")
)
CANCELATION_STATUS = (
    ("pending", "Pending"),
    ("accepted", "Accepted"),
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


def validate_expiry_date(value):
    min_date = date.today()
    if value < min_date:
        raise ValidationError(
            (f"Expiry date cannot be earlier than {min_date}.")
            )
    


    

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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,related_name="category")
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, default=None)
    image = models.ImageField(upload_to="products", default='product-icon.png')
    # description = models.TextField(null=True, default=None,blank = True)
    description = RichTextUploadingField(null=True, default=None,blank = True)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=None)
    discount_price = models.DecimalField(max_digits=100, decimal_places=2, default=None)
    stock_count = models.IntegerField(default=10)
    mfd = models.DateField(null = True,auto_now_add=False,blank=True)
    life = models.CharField(max_length=50,default=50)
    status = models.BooleanField(default=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default="published")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
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
    
    def get_offer_price_by_category(self):
        return int(self.discount_price - (self.discount_price * self.category.offer.off_percent / 100))

class ProductItem(models.Model):
    piid = ShortUUIDField(unique=True, length=10, max_length=20)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,default=None,null=True,blank=True,related_name="items")
    title = models.CharField(max_length=100, default=None)
    image = models.ImageField(upload_to="products", default='product-icon.png')
    stock_count = models.IntegerField(default=10)
    product_status = models.CharField(choices=STATUS, max_length=10, default="published")
    status = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=None)
    discount_price = models.DecimalField(max_digits=100, decimal_places=2, default=None)
    in_stock = models.BooleanField(default=True)
    sku = ShortUUIDField(unique=True, length=5, max_length=10,prefix="sku", alphabet="123456789")
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    

    class Meta:
        verbose_name_plural = "Product Items"

    def product_item_image(self):
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



class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active = True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='package_size',is_active = True)

variation_category_choice = (
    ('package_size','Package Size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True)
    variation_category = models.CharField(max_length=100,choices=variation_category_choice)
    variation_value = models.CharField(max_length=100,null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_created=True,null=True)

    objects = VariationManager()


    class Meta:
        verbose_name_plural = "Variations"

    def __str__(self):
        return self.variation_value


class Varient(models.Model):
    name = models.CharField(max_length=200,default=None,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,related_name="varient_category")
    type = models.CharField(choices=VARIENT_CHOiCE, max_length=10, default="text")

    class Meta:
        verbose_name_plural = "Varients"

    def __str__(self):
        return self.name

class VarientValue(models.Model):
    varient = models.ForeignKey(Varient,on_delete=models.SET_NULL, null=True,related_name="varient")
    value = models.CharField(max_length=200,default=None,null=True,blank=True)
    color_code = models.CharField(max_length=200,default=None,null=True,blank=True)
    image = models.ImageField(upload_to='varient-images', default=None,blank=True,null=True)

    class Meta:
        verbose_name_plural = "Varient Values"

    def varient_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

class ProductVarientLink(models.Model):
    varient = models.ForeignKey(Varient,on_delete=models.SET_NULL,related_name="prd_varient_item", null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,related_name="prd_varient", null=True)

    class Meta:
        verbose_name_plural = "Product Varient Link"

class ProductVarientConfigeration(models.Model):
    varient_value = models.ForeignKey(VarientValue,on_delete=models.SET_NULL,related_name="prd_varient_values_label", null=True)
    product_item = models.ForeignKey(ProductItem,on_delete=models.SET_NULL,related_name="prd_varient_values", null=True)

    class Meta:
        verbose_name_plural = "Product Varient Configerations"




########################  Cart, Orderitems and Address  #######################

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField()
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
    def is_expired(self):
        return self.valid_to < date.today()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=250,blank=True)
    session_id = models.CharField(max_length=200,null=True,blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Cart"

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    cart        = models.ForeignKey(Cart,related_name="cart_items",on_delete=models.CASCADE,blank=True,null=True)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True,null=True)
    variations  = models.ManyToManyField(Variation,blank=True) 
    qty         = models.PositiveIntegerField(default=1)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id  = models.CharField(max_length=200,null=True,blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)


    class Meta:
        verbose_name_plural = "Cart Items"

    def sub_total(self):
        return self.product.discount_price * self.qty
    
    def sub_total_with_offer(self):
        return int((self.sub_total()) - ( self.sub_total() * self.product.offer.off_percent / 100))
    
    def sub_total_with_offer_category(self):
        return int((self.sub_total()) - ( self.sub_total() * self.product.category.offer.off_percent / 100))
    
    def __unicode__(self):
        return self.product


class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderno = ShortUUIDField(unique=True, length=10,max_length=20, prefix="od", alphabet="1234567890")
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=None)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOCE, max_length=30, default="processing")
    payment_type = models.CharField(choices=PAYMENT_CHOiCE, max_length=30, default="cod")
    razorpay_order_id = models.CharField(max_length=100,blank=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    coupon_discount = models.DecimalField(null=True,blank=True,max_digits=100,decimal_places=2,)
    is_ordered = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Cart Order"
    
    def __str__(self):
        return self.orderno


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder,related_name="order_items",on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(choices=STATUS_CHOCE, max_length=30, default="processing")
    variations  = models.ManyToManyField(Variation,blank=True) 
    package_size = models.CharField(max_length=100,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=None)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=None)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    
class OrderAddress(models.Model):
    order = models.ForeignKey(CartOrder,on_delete=models.SET_NULL, null=True)
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

class OrderCancellationReason(models.Model):
    reason = models.CharField(max_length=255)
    status =models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.reason  

class OrderCancellation(models.Model):
    order_item = models.ForeignKey(CartOrderItems,related_name="cancellation",on_delete=models.CASCADE)
    reason = models.ForeignKey(OrderCancellationReason, on_delete=models.SET_NULL,blank=True,null=True)
    status = models.CharField(choices=CANCELATION_STATUS,default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.order_item.product.title  




    
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
    # products = models.ManyToManyField(Product)
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
    
    def save(self, *args, **kwargs):
        if self.is_default:
            # If the current address is being set as default,
            # unset 'is_default' for all other addresses of the same user.
            Address.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super(Address, self).save(*args, **kwargs)
    

class Offer(models.Model):
    name = models.CharField(max_length=50)
    off_percent = models.PositiveIntegerField()
    start_date = models.DateField(validators=[validate_expiry_date])
    category = models.OneToOneField(Category, on_delete=models.SET_NULL,blank=True,null=True)
    end_date = models.DateField()

    def __str__(self) -> str:
        return self.name




