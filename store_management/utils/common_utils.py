from rest_framework.pagination import PageNumberPagination


def get_or_none(class_model, *args, **kwargs):
    try:
        return class_model.objects.get(*args, **kwargs)
    except class_model.DoesNotExist:
        return None


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10
