from uuid import uuid4


def get_expiry_report_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"expiry_reports/{uuid4()}.{ext}"


def get_margin_report_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"margin_reports/{uuid4()}.{ext}"


def get_sales_report_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"sales_reports/{uuid4()}.{ext}"
