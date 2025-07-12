from unicodedata import category
from django.db import models

class Product(models.Model):
  sku_id = models.IntegerField(primary_key=True)
  product_id = models.CharField(max_length=255, blank=True, null=True)
  name = models.CharField(max_length=300, blank=True, null=True)
  category = models.ManyToManyField(
    'Category',
    blank=True,
    related_name='products'
  )
  brand = models.ForeignKey(
    'Brand',
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
    related_name='products'
  )
  is_transported = models.BooleanField(default=False)
  is_inventoried = models.BooleanField(default=False)
  image_url = models.URLField(blank=True, null=True)
  link_id = models.CharField(max_length=255, blank=True, null=True)
  ref_id = models.CharField(max_length=255, blank=True, null=True)
  ean = models.CharField(max_length=255, blank=True, null=True)
  sku_is_visible = models.BooleanField(default=False)
  release_date = models.DateTimeField(blank=True, null=True)
  product_is_visible = models.BooleanField(default=False)
  product_is_active = models.BooleanField(default=False)
  AlternateIdValues = models.JSONField(blank=True, null=True)
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __int__(self):
    return self.product_id

class Category(models.Model):
  category_id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=False)
  
  def __str__(self):
    return self.name

class Brand(models.Model):
  brand_id = models.IntegerField(primary_key=True)
  brand_name = models.CharField(max_length=300, blank=True, null=True)
  brand_active = models.BooleanField(default=False)
  
  def __str__(self):
    return self.brand_name

class Dimensions(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='dimensions')
  cubic_weight = models.FloatField(blank=True, null=True)
  height = models.FloatField(blank=True, null=True)
  length = models.FloatField(blank=True, null=True)
  width = models.FloatField(blank=True, null=True)
  weight = models.FloatField(blank=True, null=True)
  
class RealDimension(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='real_dimensions')
  real_cubic_weight = models.FloatField(blank=True, null=True)
  real_height = models.FloatField(blank=True, null=True)
  real_length = models.FloatField(blank=True, null=True)
  real_width = models.FloatField(blank=True, null=True)
  real_weight = models.FloatField(blank=True, null=True)
  
class ManufacturerCode(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='manufacturer')
  is_kit = models.BooleanField(default=False)
  kit_items = models.JSONField(blank=True, null=True)
  services = models.JSONField(blank=True, null=True)
  categories = models.JSONField(blank=True, null=True)

class ProductSpecifications(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_specifications')
  field_id = models.IntegerField(blank=True, null=True)
  field_value_ids = models.JSONField(blank=True, null=True)
  field_values    = models.JSONField(blank=True, null=True)