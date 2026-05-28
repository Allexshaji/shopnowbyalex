from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db.models import Avg
User=get_user_model()

class SellerProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,related_name='seller_profile')
    shop_name=models.CharField(max_length=100)
    address=models.TextField()
    pincode=models.CharField(max_length=6)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    gst_number=models.CharField(max_length=100,blank=True,null=True)
    is_verified=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    approved=models.BooleanField(default=False)
    shop_logo=models.ImageField(upload_to="seller_profile_pic/",null=True)
    def __str__(self):
        return self.shop_name

class Product(models.Model):
    seller = models.ForeignKey('seller.SellerProfile', on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=100,null=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    price = models.IntegerField()
    discount_price = models.IntegerField()

    STATUS_CHOICES = (
        ('pending', 'PENDING'),
        ('approved', 'APPROVED'),
        ('rejected', 'REJECTED'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    description = models.CharField(max_length=200)

    stock = models.PositiveIntegerField(default=1)

    available = models.BooleanField(default=True)    
    category = models.ForeignKey('seller.Category', on_delete=models.CASCADE,null=True,blank=True)
    sub_category = models.ForeignKey('seller.SubCategory', on_delete=models.CASCADE,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_primary_image(self):
        primary=self.productimage_set.filter(is_primary=True).first()        
        return primary or self.productimage_set.first()
    
    def avg_rating(self):
        return round(self.reviews_set.aggregate(Avg('rating'))['rating__avg'] or 0, 1)

    def review_count(self):
        return self.reviews_set.count()
    
class ProductAttribute(models.Model):
    product = models.ForeignKey('seller.product',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value= models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} : {self.value}"

class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, blank=True)
    image=models.ImageField(upload_to="category_icons/", null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Attribute(models.Model):
    name=models.CharField(max_length=100)
  
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('seller.Category', on_delete=models.CASCADE)
    is_active = models.BooleanField(default= True)
    slug = models.SlugField(unique=True, blank=True)
    attributes = models.ManyToManyField(Attribute,related_name='subcategories', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey('seller.Product',on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/")
    is_primary = models.BooleanField(default=False)   
    
    def __str__(self):
        return self.product.name

class VerifiedDoc(models.Model):
    document_choices=[('pan_card', 'PAN Card (Business/Personal)'),
        ('gst_certificate', 'GST Registration Certificate'),
        ('aadhar_card', 'Aadhar Card (Owner)'),
        ('trade_license', 'Trade License / Shop Act'),
        ('bank_statement', 'Canceled Cheque / Bank Statement')]
    seller=models.ForeignKey('seller.sellerprofile',on_delete=models.CASCADE)
    document_type=models.FileField(max_length=50,upload_to='verification_docs/')
    note=models.TextField(null=True,blank=True)    
        
    def __str__(self):
        return f"{self.seller.shop_name} - {self.document_type}"
    