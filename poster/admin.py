from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Image, Place


@admin.action(description='Показать изображение')
def get_preview(obj):
    return format_html('<img src="%s"' 'style="object-fit: cover; height:150px;" />' % obj.image.url)


@admin.register(Image)
class ImagesAdmin(admin.ModelAdmin):
    raw_id_fields = ('place',)
    list_display = ('place', get_preview, )
    readonly_fields = [get_preview, ]


class ImageInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Image
    fields = ['image', 'index', get_preview, ]
    readonly_fields = [get_preview, ]
    extra = 0


class PlaceAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Place
        fields = '__all__'


@admin.register(Place)
class PlacesAdmin(admin.ModelAdmin, SortableAdminMixin):
    form = PlaceAdminForm
    inlines = [ImageInline]
    list_display = ('title',)
