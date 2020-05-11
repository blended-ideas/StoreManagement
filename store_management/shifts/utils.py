from django.db.models import F

from .models import ShiftEntry
from ..products.models import ProductStockChange


def create_shift_entries_from_data(shift_detail, entries):
    for entry_data in entries:
        se = ShiftEntry.objects.create(
            shift=shift_detail,
            product_id=entry_data['product'],
            quantity=entry_data['quantity'],
        )
        se.distributor_margin = se.product.distributor_margin
        se.retailer_margin = se.product.retailer_margin
        se.price = se.product.price
        se.save()

        se.product.stock = F('stock') - se.quantity
        se.product.save()

        ProductStockChange.objects.create(
            user=shift_detail.user,
            product_id=entry_data['product'],
            value=-int(entry_data['quantity']),
            changeType='SHIFT',
            shift_entry=se
        )
