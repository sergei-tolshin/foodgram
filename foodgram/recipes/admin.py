from django import forms
from django.contrib import admin

from .models import (Favorite, Ingredient, Product, Purchase, Recipe,
                     Subscription)


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe
        widgets = {
            'tags': forms.CheckboxSelectMultiple(choices=model.TAGS_CHOICES)
        }
        fields = '__all__'


class TagsFilter(admin.SimpleListFilter):
    title = 'Теги'
    parameter_name = 'tags'

    def lookups(self, request, model_admin):
        return [
            ('breakfast', 'Завтрак'),
            ('lunch', 'Обед'),
            ('dinner', 'Ужин'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'breakfast':
            return queryset.filter(tags__contains=self.value())
        if self.value() == 'lunch':
            return queryset.filter(tags__contains=self.value())
        if self.value() == 'dinner':
            return queryset.filter(tags__contains=self.value())
        if self.value():
            return queryset.filter(tags=self.value())


class IngredientInline(admin.TabularInline):
    model = Ingredient
    fields = ('name', 'value', 'units',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'value', 'units', 'recipe')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm

    prepopulated_fields = {'slug': ('title',)}
    list_display = ('pk', 'title', 'author_name', 'pub_date')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_filter = ('author', 'title', TagsFilter)
    inlines = (IngredientInline,)
    change_form_template = 'admin/recipes/change_form_with_favorites.html'
    empty_value_display = '-пусто-'

    def author_name(self, obj):
        return obj.author.first_name or obj.author.username
    author_name.short_description = 'Автор'
    author_name.admin_order_field = 'author'

    def get_count_favorites(self, request, object_id):
        obj = self.get_object(request, object_id)
        return obj.favorites.count()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['count_favorites'] = self.get_count_favorites(
            request, object_id)
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_name', 'recipe')
    list_display_links = ('user_name',)
    empty_value_display = '-пусто-'

    def user_name(self, obj):
        return obj.user.first_name or obj.user.username
    user_name.short_description = 'Пользователь'
    user_name.admin_order_field = 'user'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_name', 'author_name')
    list_display_links = ('user_name',)
    empty_value_display = '-пусто-'

    def user_name(self, obj):
        return obj.user.first_name or obj.user.username
    user_name.short_description = 'Пользователь'
    user_name.admin_order_field = 'user'

    def author_name(self, obj):
        return obj.author.first_name or obj.author.username
    author_name.short_description = 'Автор'
    author_name.admin_order_field = 'author'


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_name', 'recipe')
    list_display_links = ('user_name',)
    empty_value_display = '-пусто-'

    def user_name(self, obj):
        return obj.user.first_name or obj.user.username
    user_name.short_description = 'Пользователь'
    user_name.admin_order_field = 'user'


admin.site.register(Product, ProductAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Purchase, PurchaseAdmin)
