from ....modules.vtex.vtex_importer import buscar_payload_sku, buscar_skus, montar_headers, processar_sku


def get_sku_context(base_url, api_key_header, api_key, app_token_header, app_token):
    sku_ids = buscar_skus()
    headers = montar_headers(api_key_header, api_key, app_token_header, app_token)

    encontrados = nao_encontrados = importados = 0

    for sku in sku_ids:
        try:
            payload = buscar_payload_sku(sku, base_url, headers)

            if not payload:
                nao_encontrados += 1
                continue

            processar_sku(payload, sku)
            encontrados += 1
            importados += 1

        except Exception as e:
            print(f"Erro ao processar SKU {sku}: {e}")
            continue

    print(f"Encontrados: {encontrados}, Não encontrados: {nao_encontrados}, Importados: {importados}")
    return {
        "success": True,
        "found": encontrados,
        "missing": nao_encontrados,
        "imported": importados
    }