from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HomePage(Page):
    image = models.ForeignKey(
        "wagtailimages.image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero = models.CharField(
        blank=True,
        verbose_name="Hero CTA",
        max_length=200,
        help_text="Text to display on CTA",
    )

    hero_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA Link",
        help_text="Choose a Link",
    )

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("hero"),
                FieldPanel("hero_link"),
            ],
            heading="Hero Section",
        ),
        FieldPanel("body"),
    ]
