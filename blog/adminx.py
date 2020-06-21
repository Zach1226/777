import xadmin

from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter

from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.adminx import BaseOwnerAdmin


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status_show', 'pv', 'uv', 'created_time',
        'operator'
    ]
    list_display_links = []

    list_filter = ['category']
    search_fields = ['title', 'category__name', 'owner_username']

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    form_layout = (
        Fieldset(
            '基础配置',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        ),
    )

    filter_vertical = ('tag', )

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>',
                           reverse('xadmin:blog_post_change', args=(obj.id, )))

    operator.short_description = '操作'

    @property
    def media(self):
        media = super().media
        return media


class PostInline:
    form_layout = (Container(Row("title", "desc"), ))
    extra = 1
    model = Post


@xadmin.sites.register(
    Category, )
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [
        PostInline,
    ]
    list_display = ('name', 'status', 'is_nav', 'created_time')
    fields = (
        'name',
        'status',
        'is_nav',
    )


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):

    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin,
                         field_path)
        self.lookup_choices = Category.objects.filter(
            owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)

# Register your models here.
