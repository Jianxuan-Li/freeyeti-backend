from django import forms
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtailcodeblock.blocks import CodeBlock
from wagtail.api import APIField

from rest_framework import fields
from wagtail.rich_text import expand_db_html


class APIRichTextSerializer(fields.CharField):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return expand_db_html(representation)


class APIRichTextField(APIField):
    def __init__(self, name):
        serializer = APIRichTextSerializer()
        super().__init__(name=name, serializer=serializer)


class LifeBlogPage(Page):
    body = RichTextField(blank=True)

    author = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField("Post date", blank=True, null=True)
    context = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("code", CodeBlock(label="Code")),
        ],
        use_json_field=True,
        blank=True,
        null=True,
    )
    view_count = models.IntegerField(blank=False, default=0, null=True)
    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("author"),
        FieldPanel("date"),
        FieldPanel("context"),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel(
            "view_count",
            widget=forms.NumberInput(attrs={"readonly": "readonly"}),
        )
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("feed_image"),
    ]

    # Export fields over the API
    api_fields = [
        APIField("author"),
        APIField("date"),
        APIRichTextField("context"),
        APIField("view_count"),
        APIField("feed_image"),
    ]


class BlogPage(Page):
    body = RichTextField(blank=True)

    author = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField("Post date", blank=True, null=True)
    context = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("code", CodeBlock(label="Code")),
        ],
        use_json_field=True,
        blank=True,
        null=True,
    )
    view_count = models.IntegerField(blank=False, default=0, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("author"),
        FieldPanel("date"),
        FieldPanel("context"),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel(
            "view_count",
            widget=forms.NumberInput(attrs={"readonly": "readonly"}),
        )
    ]

    # Export fields over the API
    api_fields = [
        APIField("author"),
        APIField("date"),
        APIRichTextField("context"),
        APIField("view_count"),
    ]


class BlogIndex(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    # Export fields over the API
    api_fields = [
        APIField("body"),
    ]


class AboutPage(Page):
    date = models.DateField("Post date", blank=True, null=True)
    context = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("code", CodeBlock(label="Code")),
        ],
        use_json_field=True,
        blank=True,
        null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("context"),
    ]

    # Export fields over the API
    api_fields = [
        APIField("date"),
        APIRichTextField("context"),
    ]
