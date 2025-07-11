from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status as drf_status

# models
from vtex.models import baseVtex
from django.db.models import Max

# secrets
from .api.secrets.secrets import BASE_URL, api_key_vtex, app_token_vtex, app_token_vtex_header, api_key_vtex_header

# api
from .api.GET.sku.get_sku_id import get_sku_list

# TODO: Criar um shedule para essa rotina salvar ids de sku de x em x tempos
# Create your views here.
@api_view(['GET'])
def get_list_sku_ids(request):
  if request.method == 'GET':
    try:
      page_size = 1000
      max_sku = baseVtex.objects.aggregate(max_id=Max('sku_id'))['max_id'] or 0
      next_page = max_sku // page_size + 1
      
      result = get_sku_list(BASE_URL, api_key_vtex_header, api_key_vtex, app_token_vtex_header, app_token_vtex, next_page, page_size)
      
      return Response({'success': True, **result}, status=drf_status.HTTP_200_OK)
      
    except Exception as e:
      return Response(status=drf_status.HTTP_400_BAD_REQUEST)
  else:
    return Response(status=drf_status.HTTP_405_METHOD_NOT_ALLOWED)