from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.get_authors, name='authors-all'),
    path('authors/<int:author_id>', views.get_one_author, name='author-one'),
    path('books/', views.BookListView.as_view(), name='books-all'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-one'),
]
