from django.forms import ModelForm, ValidationError, CharField, TextInput, Select, CheckboxSelectMultiple, \
    CheckboxInput, ModelMultipleChoiceField, SelectMultiple
from django.utils.text import slugify
from .models import Article, Tag


class ArticleForm(ModelForm):
    reserved_slugs = [ 'new', 'edit', 'admin', 'account' ]
    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=SelectMultiple,
        required=False,
    )

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


    def clean_title(self):
        title = self.cleaned_data.get('title')

        if Article.objects.filter(title__iexact=title).exists():
            raise ValidationError("An article with this title already exists. Please choose a different title.")

        slug = slugify(title)
        if slug in self.reserved_slugs:
            raise ValidationError(f"The title '{title}' is reserved. Please choose a different title.")

        return title