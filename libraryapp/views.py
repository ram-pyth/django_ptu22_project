from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse

from .models import Author, Book, BookInstance, Genre
from .forms import BookReviewForm


def index(request):
    # suskaičiuojam turimus autorius
    num_authors = Author.objects.count()

    # suskaičiuojam turimas knygas ir finzinius egzempliorius
    num_books = Book.objects.count()
    num_bookinstances = BookInstance.objects.count()

    # suskaičiuojam laisvus egzempliorius status == g
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    # skaitliukas anoniminiams vartotojams
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context_my = {'num_authors_t': num_authors,
                  'num_books_t': num_books,
                  'num_bookinstances_t': num_bookinstances,
                  'num_instances_available_t': num_instances_available,
                  'num_visits_t': num_visits
                  }

    return render(request, 'index.html', context=context_my)


def get_authors(request):
    # visos eilutės iš author lentelės
    authors = Author.objects.all()
    paginator = Paginator(authors, 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)  # porcijos nr

    context = {
        'authors': paged_authors
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
    paginate_by = 6


class BookDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Book
    context_object_name = 'book'  # book - standartinis kintamojo template pavadinimas,sukuriamas django
    template_name = 'book.html'
    form_class = BookReviewForm


def search(request):
    # žodynas su params - request.GET
    # GET['search_text'] - tekstas iš paieškos laukelio
    query_text = request.GET['search_text']
    # title - Book laukas, icontains - paieškos metodas
    search_results = Book.objects.filter(Q(title__icontains=query_text) |
                                         Q(summary__icontains=query_text) |
                                         # author - FK(Book į Author), last_name(Author)
                                         Q(author__last_name__icontains=query_text)
                                         )

    context = {'book_list': search_results,
               'query_text': query_text}
    return render(request, 'search.html', context=context)


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'user_books.html'
    context_object_name = 'bookinstance_list'

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user).filter(status='p').order_by('due_back')


@csrf_protect
def register_user(request):
    if request.method == 'GET':
        return render(request, 'registration/registration.html')
    elif request.method == 'POST':
        # paimam duomenis iš formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.warning(request, 'Slaptažodžiai nesutampa!!!')

        if User.objects.filter(username=username).exists():
            messages.warning(request, f'Vart. vardas {username} užimtas!!!!')

        if not email:
            messages.warning(request, 'Email neįvestas')

        if User.objects.filter(email=email).exists():
            messages.warning(request, f'Emailas {email} jau registruotas!!!')

        # jeigu yra nors viena žinutė messages(reiškia negalim registruoti userio)
        if messages.get_messages(request):
            return redirect('register-url')

        # jeigu nebuvo klaidų įvestoje info ir mes galim registruoti naują userį
        User.objects.create_user(username=username, email=email, password=password)
        messages.info(request, f'Vartotojas vardu {username} sukurtas!!!')
        return redirect('login')


