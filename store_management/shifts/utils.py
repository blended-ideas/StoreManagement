from django.db.models import F

from .models import ShiftEntry
from ..products.models import ProductStockChange
from ..utils.common_utils import get_or_none


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


def update_shift_entry(entry_id, new_quantity, user_id):
    shift_entry = get_or_none(ShiftEntry, id=entry_id)
    if shift_entry is None:
        return

    quantity_change = shift_entry.quantity - new_quantity
    shift_entry.quantity = new_quantity
    shift_entry.save()

    print(quantity_change)
    if quantity_change != 0:
        shift_entry.product.stock = F('stock') + quantity_change
        shift_entry.product.save()

        psc = ProductStockChange.objects.create(
            user_id=user_id,
            product=shift_entry.product,
            value=-int(quantity_change),
            changeType='SHIFT_MODIFICATION',
            shift_entry=shift_entry
        )


def create_shift_entry(entry, shift_id, user_id):
    se = ShiftEntry.objects.create(
        shift_id=shift_id,
        product_id=entry['product'],
        quantity=entry['quantity'],
    )
    se.distributor_margin = se.product.distributor_margin
    se.retailer_margin = se.product.retailer_margin
    se.price = se.product.price
    se.save()

    se.product.stock = F('stock') - se.quantity
    se.product.save()

    ProductStockChange.objects.create(
        user_id=user_id,
        product_id=entry['product'],
        value=-int(entry['quantity']),
        changeType='SHIFT',
        shift_entry=se
    )
