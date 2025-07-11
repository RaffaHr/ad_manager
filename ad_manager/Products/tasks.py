from celery import shared_task

# api
from .api.GET.sku.get_sku_id import get_sku_list
from .api.GET.sku.get_sku_ean import get_sku_ean
from .api.GET.sku.get_sku_context import get_sku_context

# models
from Products.models import Product
from django.db.models import Max

# secrets
from .api.secrets.secrets import BASE_URL, api_key_vtex, app_token_vtex, app_token_vtex_header, api_key_vtex_header

# modules
from .modules.task.task_qa import task_qa

def get_vtex_headers():
    return api_key_vtex_header, api_key_vtex, app_token_vtex_header, app_token_vtex

@shared_task
def get_list_sku_ids():
  def task():
      page_size = 1000
      max_sku = Product.objects.aggregate(max_id=Max('sku_id'))['max_id'] or 0
      next_page = max_sku // page_size + 1
      headers = get_vtex_headers()
      return get_sku_list(BASE_URL, *headers, next_page, page_size)
  return task_qa(task)

@shared_task
def get_sku_context_by_sku_id():
  def task():
      headers = get_vtex_headers()
      return get_sku_context(BASE_URL, *headers, app_token_vtex)
  return task_qa(task)