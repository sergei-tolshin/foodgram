import io
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .forms import RecipeForm
from .models import Favorite, Ingredient, Recipe, Subscription
from .utils import slugify

User = get_user_model()


def index(request):
    # теги для фильтрации по рецептам
    tag_breakfast = request.GET.get('breakfast')
    tag_lunch = request.GET.get('lunch')
    tag_dinner = request.GET.get('dinner')

    # строим фильтр по тегам
    filter_tag = Q()
    if tag_breakfast:
        filter_tag |= Q(tags__contains='breakfast')
    if tag_lunch:
        filter_tag |= Q(tags__contains='lunch')
    if tag_dinner:
        filter_tag |= Q(tags__contains='dinner')

    recipe_list = Recipe.objects.order_by('-pub_date').all()
    recipe_list = recipe_list.filter(filter_tag)

    # показывать по 6 рецептов на странице
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    data = {
        'breakfast': tag_breakfast,
        'lunch': tag_lunch,
        'dinner': tag_dinner,
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'index.html', context=data)


def profile(request, username):
    subscription = False
    profile = get_object_or_404(User, username=username)

    # теги для фильтрации по рецептам
    tag_breakfast = request.GET.get('breakfast')
    tag_lunch = request.GET.get('lunch')
    tag_dinner = request.GET.get('dinner')

    # строим фильтр по тегам
    filter_tag = Q()
    if tag_breakfast:
        filter_tag |= Q(tags__contains='breakfast')
    if tag_lunch:
        filter_tag |= Q(tags__contains='lunch')
    if tag_dinner:
        filter_tag |= Q(tags__contains='dinner')

    recipe_list = Recipe.objects.filter(author=profile).order_by('-pub_date')
    recipe_list = recipe_list.filter(filter_tag)

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        subscription = Subscription.objects.filter(
            user=request.user, author=profile).first()

    data = {
        'breakfast': tag_breakfast,
        'lunch': tag_lunch,
        'dinner': tag_dinner,
        'profile': profile,
        'page': page,
        'paginator': paginator,
        'subscription': subscription,
    }
    return render(request, 'profile.html', context=data)


def view_recipe(request, slug, recipe_id):
    subscription = False
    favorite = False

    recipe = get_object_or_404(Recipe, id=recipe_id, slug=slug,)

    if request.user.is_authenticated:
        subscription = Subscription.objects.filter(
            user=request.user, author=recipe.author).first()

        favorite = Favorite.objects.filter(
            user=request.user, recipe=recipe).first()

    data = {
        'recipe': recipe,
        'subscription': subscription,
        'favorite': favorite,
    }
    return render(request, 'recipe.html', context=data)


@login_required
def new_recipe(request):
    if request.method == 'POST':

        form = RecipeForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.slug = slugify(recipe.title)
            recipe.save()
            form.add_ingredients()
            return redirect('index')

        return render(request, 'new_recipe.html', {'form': form})

    form = RecipeForm()
    return render(request, 'new_recipe.html', {'form': form, })


@login_required
def edit_recipe(request, slug, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, slug=slug)

    if recipe.author != request.user:
        return redirect('recipe', slug=recipe.slug, recipe_id=recipe_id)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe)

    if request.method == 'POST':
        if form.is_valid():
            recipe.save()
            form.add_ingredients()
            return redirect('recipe', slug=recipe.slug, recipe_id=recipe_id)

    return render(request, 'new_recipe.html', {'form': form, 'recipe': recipe})


@login_required
def delete_recipe(request, slug, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, slug=slug)
    if recipe.author != request.user:
        return redirect('recipe', slug=recipe.slug, recipe_id=recipe_id)

    recipe.delete()

    return redirect('index')


@login_required
def subscriptions(request):
    profile = get_object_or_404(User, username=request.user)
    subscription_list = profile.subscriptions.all()

    paginator = Paginator(subscription_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'subscriptions.html', context=data)


@login_required
def favorites(request):
    profile = request.user

    # теги для фильтрации по рецептам
    tag_breakfast = request.GET.get('breakfast')
    tag_lunch = request.GET.get('lunch')
    tag_dinner = request.GET.get('dinner')

    # строим фильтр по тегам
    filter_tag = Q()
    if tag_breakfast:
        filter_tag |= Q(recipe__tags__contains='breakfast')
    if tag_lunch:
        filter_tag |= Q(recipe__tags__contains='lunch')
    if tag_dinner:
        filter_tag |= Q(recipe__tags__contains='dinner')

    favorite_list = profile.favorites.all()
    favorite_list = favorite_list.filter(
        filter_tag).order_by('-recipe__pub_date')

    paginator = Paginator(favorite_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {
        'breakfast': tag_breakfast,
        'lunch': tag_lunch,
        'dinner': tag_dinner,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'favorites.html', context=data)


def purchases(request):
    if request.user.is_authenticated:
        profile = request.user
        recipes_list = Recipe.objects.filter(
            pk__in=profile.purchases.values('recipe')
        )
    else:
        request.session.setdefault('purchases', [])
        recipes_list = Recipe.objects.filter(
            pk__in=request.session['purchases']
        )

    data = {
        'recipes': recipes_list,
    }
    return render(request, 'purchases.html', context=data)


# формирование PDF документа со списком покупок
def purchases_to_pdf(request):
    today = datetime.today().strftime('%d-%m-%Y')

    if request.user.is_authenticated:
        profile = request.user
        ingredients = Ingredient.objects.filter(
            recipe__in=profile.purchases.values('recipe')
        ).values('name', 'units').annotate(Sum('value')).order_by('name')
    else:
        ingredients = Ingredient.objects.filter(
            recipe__in=request.session['purchases']
        ).values('name', 'units').annotate(Sum('value')).order_by('name')

    buffer = io.BytesIO()

    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont('Arial', 16, leading=None)
    p.drawString(10*mm, 277*mm, 'Список покупок')
    p.line(10*mm, 272*mm, 200*mm, 272*mm)

    y = 267*mm
    for i, item in enumerate(ingredients, 1):
        p.setFont('Arial', 14, leading=None)
        p.drawString(
            20*mm, y-5*mm,
            f'{i}. {item["name"]} - {item["value__sum"]} {item["units"]}')
        y = y-8*mm

    p.line(10*mm, 10*mm, 200*mm, 10*mm)
    p.setFont('Arial', 10, leading=None)
    p.drawString(10*mm, 5*mm, today)
    p.drawRightString(200*mm, 5*mm, 'Продуктовый помощник')

    p.setTitle(f'Список покупок от {today}')
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True,
                        filename='Список покупок.pdf')


# вывод страницы при ошибке 404
def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


# вывод страницы при ошибке 500
def server_error(request):
    return render(request, 'misc/500.html', status=500)
