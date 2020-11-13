from django.db.models import Q
from django.template.defaultfilters import slugify as django_slugify

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
            'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k',
            'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
            'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
            'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


# транслитерация для slug
def slugify(s):
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


# строим фильтр по тегам
def get_filter_tags(request):
    filter_tag = Q()
    if request.GET.get('breakfast'):
        filter_tag |= Q(tags__contains='breakfast')
    if request.GET.get('lunch'):
        filter_tag |= Q(tags__contains='lunch')
    if request.GET.get('dinner'):
        filter_tag |= Q(tags__contains='dinner')

    return filter_tag
