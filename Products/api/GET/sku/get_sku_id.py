import requests
from Products.models import Product

def get_sku_list(base_url: str, api_key_vtex_header: str, api_key_vtex: str, app_token_vtex_header: str, app_token_vtex: str ,page: int, page_size: int) -> list:
  url = f"{base_url}api/catalog_system/pvt/sku/stockkeepingunitids?page={page}&pagesize={page_size}"

  print(url)
  print(f"pagina: {page}")
  
  headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    api_key_vtex_header: api_key_vtex,
    app_token_vtex_header: app_token_vtex
  }
  
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    import_sku_id = 0
    
    for _ in data:
      Product.objects.update_or_create(sku_id=_)
      import_sku_id += 1
    
    print(f'Foram importados: {import_sku_id}')
    
    return {"success": True, "imported": import_sku_id}
  
  except requests.exceptions.RequestException as e:
      return {"success": False, "Error": str(e)}
  except ValueError as ve:
    return {"success": False, "Error": str(ve)}