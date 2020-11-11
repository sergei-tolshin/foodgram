from django import template
from recipes.models import Favorite, Purchase, Recipe

register = template.Library()


# добавление класса полю формы
@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


# проверка наличия рецепта в избранных
@register.filter
def in_favorites(user, recipe):
    return Favorite.objects.filter(user=user, recipe=recipe).first()


# изменение формы слов в зависимости от числа
@register.filter
def rupluralize(value, arg):
    args = arg.split(',')
    number = abs(int(value))
    a = number % 10
    b = number % 100

    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
    else:
        return args[2]


# сбор строки GET параметров
@register.simple_tag
def add_query_params(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v:
            updated[k] = v
        else:
            updated.pop(k)

    return request.build_absolute_uri('?' + updated.urlencode())


# проверка рецепта в списке покупок
@register.simple_tag
def in_purchases(request, recipe_id):
    if request.user.is_authenticated:
        return Purchase.objects.filter(user=request.user,
                                       recipe=recipe_id).first()
    else:
        purchases = request.session.get('purchases', [])
        return recipe_id in purchases


# счетчик списка покупок
@register.simple_tag
def purchase_counter(request):
    counter = 0

    if request.user.is_authenticated:
        user = request.user
        counter = user.purchases.count()
    else:
        # счетчик пересчитывается на случай, если рецепт был удален
        purchases = request.session.get('purchases', [])
        counter = Recipe.objects.filter(pk__in=purchases).count()

    return counter
