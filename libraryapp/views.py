from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse

from .models import Author, Book, BookInstance, Genre


def index(request):
    # suskaičiuojam turimus autorius
    num_authors = Author.objects.count()

    # suskaičiuojam turimas knygas ir finzinius egzempliorius
    num_books = Book.objects.count()
    num_bookinstances = BookInstance.objects.count()

    # suskaičiuojam laisvus egzempliorius status == g
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    context_my = {'num_authors_t': num_authors,
                  'num_books_t': num_books,
                  'num_bookinstances_t': num_bookinstances,
                  'num_instances_available_t': num_instances_available
                  }

    return render(request, 'index.html', context=context_my)


def get_authors(request):
    # visos eilutės iš author lentelės
    authors = Author.objects.all()

    context = {
        'authors': authors
    }
    return render(request, 'authors.html', context=context)


def get_one_author(request, author_id):
    # author_id - integer, pagal jį ieškom author lentelėj eilutės
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author.html', {'author_obj': single_author})


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'  # book_list - standartinis kintamojo template pavadinimas,sukuriamas django
    template_name = 'books.html'


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'  # book - standartinis kintamojo template pavadinimas,sukuriamas django
    template_name = 'book.html'

