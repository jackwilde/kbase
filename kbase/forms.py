from django.core.validators import RegexValidator
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
                'placeholder': 'Article title',
            }),
            'content': Textarea(attrs={
                'id': 'input-content',
                'placeholder': 'Enter article content here.',
            }),
            'tags': SelectMultiple(attrs={
                'id': 'input-tags',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update the choices for the 'tags' field to use tag names as values
        self.fields['tags'].widget.choices = [(tag.tag, tag.tag) for tag in Tag.objects.all()]

        if self.instance.pk:  # Only if it's an existing article (editing mode)
            # Set the initial value of the 'tags' field to the current tags associated with the article
            self.initial['tags'] = [tag.tag for tag in self.instance.tags.all()]

        self.tag_errors = []

    def is_valid(self):
        # Tags need to be updated before validation to allow new tags to be created
        self.update_tags()
        return super().is_valid()


    def clean_title(self):
        title = self.cleaned_data.get('title')
        article_id = self.instance.id

        if Article.objects.filter(title__iexact=title).exclude(id=article_id).exists():
            raise ValidationError("An article with this title already exists. Please choose a different title.")

        slug = slugify(title)
        if slug in self.reserved_slugs:
            raise ValidationError(f"The title '{title}' is reserved. Please choose a different title.")

        return title


    def update_tags(self):
        """
        Validates tag entry and adds new tags to database if required
        :return:
        """
        # Get the tags submitted on the form. If an existing tag is selected the value will be the id, else the tag name
        tags = self.data.getlist('tags')
        if tags:
            tag_list = []
            for tag in tags:
                # If the tag is alphanumeric create it or return the existing tag
                if tag.isalnum():
                    tag_instance, created = Tag.objects.get_or_create(tag=tag)
                    # Add tag ids to list
                    tag_list.append(tag_instance)
                # If not add the tag string to the list for validation at clean stage
                else:
                    self.tag_errors.append(f'{tag} contains non alphanumeric characters.')
                    #TODO how can we let the user know they've done this and we're ignoring it

            # Create a copy of the data to edit and update with the new list
            data_copy = self.data.copy()
            data_copy.setlist('tags', tag_list)

            # Set the edited data
            self.data = data_copy


