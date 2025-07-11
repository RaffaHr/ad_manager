import requests
from vtex.models import baseVtex
from django.db.models import Max

def get_sku_list(base_url: str, api_key_vtex_header: str, api_key_vtex: str, app_token_vtex_header: str, app_token_vtex: str ,page: int, page_size: int) -> list:
  url = f"{base_url}sku/stockkeepingunitids?page={page}&pagesize={page_size}"

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
      baseVtex.objects.update_or_create(sku_id=_)
      import_sku_id += 1
    
    print(f'Foram importados: {import_sku_id}')
    
    return {'success': True}
  
  except requests.exceptions.RequestException as e:
    print(f"Erro na solicitação: {e}")
    return None
  except ValueError as ve:
    print(f"Erro ao decodificar JSON: {ve}")
    return None