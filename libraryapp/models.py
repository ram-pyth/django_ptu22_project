from django.db import models
from django.contrib.auth.models import User

from tinymce.models import HTMLField
from datetime import date
import uuid
import PIL


class Author(models.Model):
    """Autorių lentelės klasė
    reprezentuojanti vieną autorių"""
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)
    # description = models.TextField('Aprašymas', max_length=2000, default="biografija...")
    description = HTMLField()

    class Meta:  # globalūs nuostatai lentelei(ordering - rikiavimas)
        ordering = ('last_name', 'first_name')

    def __str__(self):
        """Objekto vaizdavimas stringu"""
        return f'{self.last_name} {self.first_name}'

    def display_books(self):  # book_set - relationshipas į Book, automatiškai sudaromas django
        return ', '.join(elem.title for elem in self.book_set.all()[:3]) + ' ...'


class Genre(models.Model):
    name = models.CharField("Žanrai", max_length=15, help_text='Įveskite knygos žanrą/us')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Žanras'  # skilties pavadinimas vienaskaita
        verbose_name_plural = 'Žanrai'  # skilties pavadinimas daugiskaita


class Book(models.Model):
    """Viena knyga, autoriai turi ne po vieną
    todėl čia apsirašysim Foreign Key"""
    title = models.CharField('Pavadinimas', max_length=150)
    summary = models.TextField('Aprašymas', max_length=1000)
    isbn = models.CharField('ISBN', max_length=13)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, blank=True)
    cover = models.ImageField('Viršelis', upload_to='covers', null=True, blank=True)

    def __str__(self):
        return self.title

    def display_genres(self):
        return ', '.join(elem.name for elem in self.genre.all())


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    due_back = models.DateField('Bus prieinama', null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # statusų rinkinys(ne db stulpelis)
    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota')
    )

    # pats lentelės stulpelis, kuris naudos statusų rinkinį
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,  # blank - galimas tuščias laukas formoj
        default='a',
        help_text='Knygos kopijos statusas'
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        else:
            return False

    def __str__(self):
        return f'{self.id} {self.status} {self.due_back} {self.book} {self.book.author}'


class BookReview(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             blank=True)  # blank True, nes formoje nerodysim pasirinkimo knygos
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.date_created}, {self.reviewer}, {self.book}, {self.content[:50]}'


class Profile(models.Model):
    picture = models.ImageField(upload_to='profile_pics', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} profilis'
