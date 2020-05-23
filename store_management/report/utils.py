from uuid import uuid4


def get_expiry_report_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"expiry_reports/{uuid4()}.{ext}"
