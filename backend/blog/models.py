from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField

from rest_framework import fields
from wagtail.core.rich_text import expand_db_html


class APIRichTextSerializer(fields.CharField):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return expand_db_html(representation)

class APIRichTextField(APIField):
    def __init__(self, name):
        serializer = APIRichTextSerializer()
        super().__init__(name=name, serializer=serializer)

class BlogPage(Page):
    body = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    # Export fields over the API
    api_fields = [
        APIRichTextField('body'),
    ]

class BlogIndex(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    # Export fields over the API
    api_fields = [
        APIField('body'),
    ]