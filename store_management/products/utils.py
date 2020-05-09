from uuid import uuid4


def get_product_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"product_images/{uuid4()}.{ext}"
