from django.db import models

# Create your models here.
class baseVtex(models.Model):
  sku_id = models.IntegerField(primary_key=True)
  product_id = models.CharField(max_length=255, blank=True, null=True)
  name = models.CharField(max_length=300, blank=True, null=True)
  category_id = models.IntegerField(blank=True, null=True)
  brand_id = models.IntegerField(blank=True, null=True)
  link_id = models.CharField(max_length=255, blank=True, null=True)
  ref_id = models.CharField(max_length=255, blank=True, null=True)
  ean = models.CharField(max_length=255, blank=True, null=True)
  is_visible = models.BooleanField(default=False)
  release_date = models.DateTimeField(blank=True, null=True)
  title = models.CharField(max_length=255, blank=True, null=True)
  is_active = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.product_id
