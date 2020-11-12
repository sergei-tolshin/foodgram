import posixpath

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from .models import Ingredient, Recipe


# виджет для отображения кнопки добавления изображения
class ImageWidget(forms.widgets.ClearableFileInput):
    template_name = 'widgets/image_file_input.html'


class RecipeForm(forms.ModelForm):
    tags = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'image', 'time', 'tags')
        labels = {
            'title': 'Название рецепта',
            'description': 'Описание',
            'image': 'Загрузить фото',
            'time': 'Время приготовления',
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 8,
            }),
            'image': ImageWidget
        }

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)

        self.fields['breakfast'] = forms.BooleanField(
            required=False, initial='breakfast' in self.instance.tags)
        self.fields['lunch'] = forms.BooleanField(
            required=False, initial='lunch' in self.instance.tags)
        self.fields['dinner'] = forms.BooleanField(
            required=False, initial='dinner' in self.instance.tags)

        for field_name in self.data:
            if (
                field_name.startswith('nameIngredient_')
                or field_name.startswith('unitsIngredient_')
            ):
                self.fields[field_name] = forms.CharField(
                    required=False, widget=forms.HiddenInput())
            if (field_name.startswith('valueIngredient_')):
                self.fields[field_name] = forms.FloatField(
                    required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(RecipeForm, self).clean()
        cleaned_data['tags'] = self.get_tags()
        cleaned_data['ingredients'] = self.get_ingredients(
            cleaned_data)
        if not cleaned_data['ingredients']:
            self.add_error(None, 'Добавьте ингредиенты')
        if not cleaned_data['tags']:
            self.add_error('tags', 'Добавьте тег')
        return cleaned_data

    def add_ingredients(self):
        recipe = self.instance
        recipe.ingredients.all().delete()
        for ingredient in self.cleaned_data['ingredients']:
            Ingredient.objects.create(
                recipe=recipe,
                name=ingredient['name'],
                value=ingredient['value'],
                units=ingredient['units'],
            )

    def get_ingredients(self, data):
        ingredients = list()
        for key in dict(data.items()):
            if 'nameIngredient' in key:
                ingredient_num = key.split('_')[1]
                ingredient = {
                    'id': ingredient_num,
                    'name': data[f'nameIngredient_{ingredient_num}'],
                    'value': data[f'valueIngredient_{ingredient_num}'],
                    'units': data[f'unitsIngredient_{ingredient_num}']
                }
                ingredients.append(ingredient)
        return ingredients

    def get_ingredient_fields(self):
        ingredients = self.get_ingredients(self.data)

        if not self.errors:
            ingredients += list(Ingredient.objects.filter(recipe=self.instance)
                                .values())

        for ingredient in ingredients:
            yield ingredient

    def get_tags(self):
        tags = list()

        if 'breakfast' in dict(self.data.items()):
            tags.append('breakfast')
        if 'lunch' in dict(self.data.items()):
            tags.append('lunch')
        if 'dinner' in dict(self.data.items()):
            tags.append('dinner')

        return tags
