from django.contrib import admin
from .models import Author, Book, Genre, BookInstance


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'author', 'display_genre')


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'id', 'status', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        ('Knyga', {'fields': ['book']}),
        ('Prieinamumas', {'fields': ['status', 'due_back']})
    )


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
