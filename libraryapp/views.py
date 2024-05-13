from django.shortcuts import render
from django.http import HttpResponse

from .models import Author, Book, BookInstance, Genre


def index(request):
    # suskaičiuojam turimus autorius
    num_authors = Author.objects.count()

    context_my = {'num_authors_t': num_authors}

    return render(request, 'index.html', context=context_my)
