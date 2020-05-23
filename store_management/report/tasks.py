from config import celery_app
from .models import ExpiryReport, MarginReport, SalesReport


@celery_app.task()
def report_cleanup():
    """Celery Task to run every night to clean up report data."""
    ExpiryReport.objects.all().delete()
    MarginReport.objects.all().delete()
    SalesReport.objects.all().delete()
