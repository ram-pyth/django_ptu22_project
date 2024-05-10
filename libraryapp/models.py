from django.db import models


class Author(models.Model):
    """Autorių lentelės klasė
    reprezentuojanti vieną autorių"""
    first_name = models.CharField('Vardas', max_length=100)
    last_name = models.CharField('Pavardė', max_length=100)

    def __str__(self):
        """Objekto vaizdavimas stringu"""
        return f'{self.last_name} {self.first_name}'


class Book(models.Model):
    """Viena knyga, autoriai turi ne po vieną
    todėl čia apsirašysim Foreign Key"""
    title = models.CharField('Pavadinimas', max_length=150)
    summary = models.TextField('Aprašymas', max_length=1000)
    isbn = models.CharField('ISBN', max_length=13)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

