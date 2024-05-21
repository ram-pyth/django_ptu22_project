from django.contrib import admin
from .models import Author, Book, Genre, BookInstance


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0  # automatiškai kuriamų papildomų eilučių skaičius


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'author', 'display_genres')
    search_fields = ('title', 'author__last_name')  # <FK>__<tėvinės laukas>
    inlines = (BookInstanceInline,)


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'id', 'reader', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    search_fields = ('id', 'book__title')
    list_editable = ('status', 'due_back', 'reader')

    fieldsets = (
        ('Knyga', {'fields': ['book']}),
        ('Prieinamumas', {'fields': ['reader', 'status', 'due_back']})
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'display_books')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
