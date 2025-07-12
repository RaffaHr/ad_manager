import requests
from Products.models import (
    Product, Category, Brand,
    Dimensions, RealDimension,
    ManufacturerCode, ProductSpecifications
)


def montar_headers(api_key_header, api_key, app_token_header, app_token):
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        api_key_header: api_key,
        app_token_header: app_token
    }


def buscar_skus():
    return list(
        Product.objects
            .filter(product_id__isnull=True)
            .order_by('sku_id')
            .values_list('sku_id', flat=True)[:5]
    )


def buscar_payload_sku(sku, base_url, headers):
    url = f"{base_url}api/catalog_system/pvt/sku/stockkeepingunitbyid/{sku}"
    resp = requests.get(url, headers=headers)

    if resp.status_code == 404:
        return None

    resp.raise_for_status()
    return resp.json()


def processar_sku(payload, sku):
    # 1) Brand
    brand_obj, _ = Brand.objects.update_or_create(
        brand_id=int(payload.get("BrandId") or 0),
        defaults={
            "brand_name": payload.get("BrandName", ""),
            "brand_active": payload.get("IsBrandActive", False)
        }
    )

    # 2) Categorias
    categories = payload.get("ProductCategories", {}) or {}
    category_objs = []
    for cat_id_str, cat_name in categories.items():
        cat_id = int(cat_id_str)
        category, _ = Category.objects.update_or_create(
            category_id=cat_id,
            defaults={"name": cat_name, "is_active": True}
        )
        category_objs.append(category)

    # 3) Produto
    prod, _ = Product.objects.update_or_create(
        sku_id=sku,
        defaults={
            "product_id": payload.get("ProductId"),
            "name": payload.get("ProductName"),
            "brand": brand_obj,
            "is_transported": payload.get("IsTransported", False),
            "is_inventoried": payload.get("IsInventoried", False),
            "image_url": payload.get("ImageUrl"),
            "link_id": payload.get("DetailUrl"),
            "ref_id": payload.get("AlternateIds", {}).get("RefId"),
            "ean": payload.get("AlternateIds", {}).get("Ean"),
            "sku_is_visible": payload.get("IsActive", False),
            "release_date": payload.get("ReleaseDate"),
            "product_is_visible": payload.get("ProductIsVisible", False),
            "product_is_active": payload.get("IsProductActive", False),
            "AlternateIdValues": payload.get("AlternateIdValues"),
        }
    )
    prod.category.set(category_objs)

    # 4) Dimensões
    dim = payload.get("Dimension", {})
    Dimensions.objects.update_or_create(
        product=prod,
        defaults={
            "cubic_weight": dim.get("cubicweight"),
            "height": dim.get("height"),
            "length": dim.get("length"),
            "width": dim.get("width"),
            "weight": dim.get("weight"),
        }
    )

    rdim = payload.get("RealDimension", {})
    RealDimension.objects.update_or_create(
        product=prod,
        defaults={
            "real_cubic_weight": rdim.get("realCubicWeight"),
            "real_height": rdim.get("realHeight"),
            "real_length": rdim.get("realLength"),
            "real_width": rdim.get("realWidth"),
            "real_weight": rdim.get("realWeight"),
        }
    )

    # 5) ManufacturerCode
    ManufacturerCode.objects.update_or_create(
        product=prod,
        defaults={
            "is_kit": payload.get("IsKit", False),
            "kit_items": payload.get("KitItems"),
            "services": payload.get("Services"),
            "categories": payload.get("Categories"),
        }
    )

    # 6) Especificações
    prod.product_specifications.all().delete()
    for spec in payload.get("ProductSpecifications", []):
        ProductSpecifications.objects.create(
            product=prod,
            field_id=spec.get("FieldId"),
            field_value_ids=spec.get("FieldValueIds"),
            field_values=spec.get("FieldValues"),
        )
