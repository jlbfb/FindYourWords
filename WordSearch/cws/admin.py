# flake8: noqa

# from django.conf import settings
from django.contrib import admin
from django.utils.html import mark_safe
from .models import (
    Word,
    WordCollection,
    CollectionGrid,
    GridMap,
)


class WordInline(admin.TabularInline):
    # This class brings the linked words into the Word Collection
    # (Word has a foreign key reference to WordCollection model)
    model = Word

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 1
        else:
            return 5

    show_change_link = True
    # Use fk_name when there is more than one foreign key in the model
    fk_name = 'word_collections'


class WordAdmin(admin.ModelAdmin):
    search_fields = ['word', 'word_collections__word_collection']
    # raw_id_fields = ['word_collections']
    list_display = ('safe_word', 'word_collections')
    # list_display_links = ('word',)
    # list_editable = ('word',)

    def safe_word(self, word):
        return mark_safe(f'<em>{word}</em>')

    class Meta:
        model = Word


class WordCollectionAdmin(admin.ModelAdmin):
    search_fields = ['word_collection']

    class Meta:
        model = WordCollection

    # This inlines reference is used to pull the linked words from Word
    # model into the Word Collection admin pages
    inlines = [WordInline,]


# class CollectionGridAdmin(admin.ModelAdmin):


class MyAdminSite(admin.AdminSite):

    def get_urls(self):
        urlpatterns = super().get_urls()
        urlpatterns += [
            # add later
        ]
        return urlpatterns


admin.site = MyAdminSite()

# Because we're defining our own MyAdminSite class, we need to register
# User and Group to the admin explicitly
from django.contrib.auth.admin import User, UserAdmin, Group, GroupAdmin
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)

admin.site.register(Word, WordAdmin)
admin.site.register(WordCollection, WordCollectionAdmin)
admin.site.register(CollectionGrid)
admin.site.register(GridMap)

admin.site.site_header = 'Find Your Words'
admin.site.site_title = 'Find Your Words Admin'
admin.site.index_title = 'Administration Panel'
