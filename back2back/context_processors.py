from .structure import CATEGORIES


def categories(request):
    return {'CATEGORIES': CATEGORIES}
