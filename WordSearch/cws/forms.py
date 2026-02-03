from django import forms
# from cws.models import WordCollection, Word


# Forms go here
class WordsForm(forms.Form):
    words = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter one word per line or separate your words '
                       'with a space or special character',
        'style': 'resize:none'}))

    # class Meta:
    #     model = Word


class WordCollectionForm(forms.Form):
    word_collection = forms.CharField(label='Word Collection Name')

    # class Meta:
    #     model = WordCollection
    #     fields = '__all__'
