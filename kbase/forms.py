from django.forms import ModelForm, ValidationError, TextInput, SelectMultiple, Textarea
from django.utils.text import slugify
from .models import Article, Tag


class ArticleForm(ModelForm):
    reserved_slugs = [ 'new', 'edit', 'admin', 'account' ]
    class Meta:
        model = Article
        fields = [
            'title',
            'tags',
            'content'
        ]
        labels = {
            'title': 'Title',
            'tags': 'Tags',
            'content': 'Article'
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
            }),
            'content': Textarea(attrs={
                'id': 'input-content',
            }),
            'tags': SelectMultiple(attrs={
                'id': 'input-tags',
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
