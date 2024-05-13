from django.db import models
import uuid


class Author(models.Model):
    """Autorių lentelės klasė
    reprezentuojanti vieną autorių"""
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)

    class Meta:  # globalūs nuostatai lentelei
        ordering = ('last_name', 'first_name')

    def __str__(self):
        """Objekto vaizdavimas stringu"""
        return f'{self.last_name} {self.first_name}'


class Genre(models.Model):
    name = models.CharField("Žanrai", max_length=15, help_text='Įveskite knygos žanrą/us')

    def __str__(self):
        return self.name


class Book(models.Model):
    """Viena knyga, autoriai turi ne po vieną
    todėl čia apsirašysim Foreign Key"""
    title = models.CharField('Pavadinimas', max_length=150)
    summary = models.TextField('Aprašymas', max_length=1000)
    isbn = models.CharField('ISBN', max_length=13)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return self.title

    def display_genre(self):
        res = ', '.join(elem.name for elem in self.genre.all())
        return res


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    due_back = models.DateField('Bus prieinama', null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

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

    def __str__(self):
        return f'{self.id} {self.status} {self.due_back} {self.book} {self.book.author}'
