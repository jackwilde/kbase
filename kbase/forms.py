from django.core.validators import RegexValidator
from django.forms import ModelForm, ValidationError, TextInput, SelectMultiple, Textarea
from django.utils.text import slugify

from .models import Article


class ArticleForm(ModelForm):
    reserved_slugs = [ 'new', ]
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'groups_with_view',
            'groups_with_edit'
        ]
        labels = {
            'title': 'Title',
            'content': 'Article',
            'groups_with_view': 'Visibility',
            'groups_with_edit': 'Editors'
        }
        error_messages = {
            'title': {
                'unique': 'An article with this title already exists.',
                'required': 'Article title is required',
            },
        }
        widgets = {
            'title': TextInput(attrs={
                'id': 'input-title',
                'placeholder': 'Article title',
            }),
            'content': Textarea(attrs={
                'id': 'input-content',
                'placeholder': 'Enter article content here.',
            }),
            'groups_with_view': SelectMultiple(attrs={
                'id': 'input-viewers',
            }),
            'groups_with_edit': SelectMultiple(attrs={
                'id': 'input-editors',
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        article_id = self.instance.id

        if Article.objects.filter(title__iexact=title).exclude(id=article_id).exists():
            raise ValidationError("An article with this title already exists. Please choose a different title.")

        slug = slugify(title)
        if slug in self.reserved_slugs:
            raise ValidationError(f"The title '{title}' is reserved. Please choose a different title.")

        return title