from django.db.models import F

from ..products.models import ProductStockChange


def create_shift_entries_from_data(shift_detail, entries):
    create_objects = list(
        map(lambda entry_data: ProductStockChange(
            user=shift_detail.user,
            product_id=entry_data['product'],
            value=-int(entry_data['quantity']),
            changeType='SHIFT',
            shift=shift_detail
        ), entries)
    )

    pscs = ProductStockChange.objects.bulk_create(create_objects)

    for psc in pscs:
        psc.product.stock = F('stock') + psc.value
        psc.product.save()
