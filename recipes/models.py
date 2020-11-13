import ast

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


# поле для хранения данных в формате списка
class ListField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        if isinstance(value, str):
            return value.split(',')

    def to_python(self, value):
        if not value:
            value = []
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        if value is not None and isinstance(value, str):
            return value
        if isinstance(value, list):
            return ','.join(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)


class Product(models.Model):
    title = models.CharField('Название', max_length=200, db_index=True)
    dimension = models.CharField('Еденицы измерения', max_length=20)

    def __str__(self):
        return f'{self.title} {self.dimension}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Recipe(models.Model):
    TAGS_CHOICES = (
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
    )

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор',
        related_name='recipes')
    title = models.CharField('Название рецепта', max_length=200)
    slug = models.SlugField(unique=False, max_length=200, db_index=True)
    tags = ListField('Теги', max_length=200)
    time = models.PositiveIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(1), MaxValueValidator(999)])
    description = models.TextField('Описание')
    image = models.ImageField('Фото', upload_to='recipes/')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    value = models.FloatField(
        'Количество',
        validators=[MinValueValidator(0), MaxValueValidator(9999)])
    units = models.CharField('Единицы измерения', max_length=20)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт',
        related_name='ingredients')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь',
        related_name='favorites')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт',
        related_name='favorites')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь',
        related_name='subscriptions')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор',
        related_name='subscribers')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Purchase(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь',
        related_name='purchases')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт',
        related_name='purchases')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
