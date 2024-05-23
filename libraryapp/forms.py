from django import forms

from .models import BookReview, Profile, User


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
