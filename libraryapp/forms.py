from django import forms

from .models import BookReview, Profile, User, BookInstance


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reviewer')
        widgets = {  # paslepiam laukus, kad jie nebūtų rodomi formoje
            'book': forms.HiddenInput(),
            'reviewer': forms.HiddenInput()
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture',)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class DateInput(forms.DateInput):
    input_type = 'date'


class UserBookInstanceCreateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ('book', 'reader', 'due_back', 'status')
        widgets = {
            'reader': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'due_back': DateInput()
        }
