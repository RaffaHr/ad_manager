import requests
from Products.models import Product

def get_sku_ean(base_url: str, api_key_vtex_header: str, api_key_vtex: str, app_token_vtex_header: str, app_token_vtex: str) -> list:
  
  sku_id_list = list(Product.objects.filter(ean__isnull=True).values_list('sku_id', flat=True).distinct().order_by('sku_id')[:25])
  
  print(sku_id_list)
  
  data = [(sku_id, None) for sku_id in sku_id_list]
  
  update_data = []
  
  eans_recuperados = 0
  eans_nao_encontrados = 0
  # loop para recuperar o ean de cada sku_id que nao possui o mesmo no banco
  for sku_id, _ in data:
    url = f"{base_url}api/catalog/pvt/stockkeepingunit/{sku_id}/ean"
    
    headers = {
      "Content-Type": "application/json",
      "Accept": "application/json",
      api_key_vtex_header: api_key_vtex,
      app_token_vtex_header: app_token_vtex
    }
    
    try:
      response = requests.get(url, headers=headers)
      response.raise_for_status()
      
      payload = response.json()
      ean = payload[0] if payload else "EAN não encontrado"
      
      if ean == "EAN não encontrado":
        eans_nao_encontrados += 1
        eans_recuperados -= 1
      
      eans_recuperados += 1
      update_data.append((sku_id, ean))
    
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}
    except ValueError as ve:
      return {"success": False, "error": str(ve)}


  eans_importados = 0
  for sku_id, ean in update_data:
    Product.objects.update_or_create(sku_id=sku_id, defaults={"ean":ean})
    eans_importados += 1
    
  print(f'Foram recuperados: {eans_recuperados} eans e {eans_importados} foram importados')

  return {'success': True}