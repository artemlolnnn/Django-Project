from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(Book)
#admin.site.register(BookInstance)
#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)

class BookInstanceInLine(admin.TabularInline):
    model = BookInstance

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = [
        'first_name',
        'last_name',
        (
        'date_of_birth',
        'date_of_death'
    )]

admin.site.register(Author, AuthorAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'display_author')
    list_filter = ('genre', 'author')
    inlines = [BookInstanceInLine]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('book', 'status')
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    fieldsets = [
        ('Book', {
            'fields': ('book', 'imprint', 'inv_nom')
        }),
        ('Status', {
            'fields': ('status', 'due_back')
        })
    ]
