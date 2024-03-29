from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
)
from wagtail.contrib.settings.models import BaseGenericSetting

from wagtail.snippets.models import register_snippet


# Create your models here.
@register_setting
class Navigation(BaseGenericSetting):
    instagram = models.URLField(verbose_name="Twitter URL", blank=True)
    github = models.URLField(verbose_name="Github URL", blank=True)
    panels = [
        MultiFieldPanel(
            [FieldPanel("instagram"), FieldPanel("github")],
            "Socials ",
        )
    ]


@register_snippet
class FooterText(
    DraftStateMixin, RevisionMixin, PreviewableMixin, TranslatableMixin, models.Model
):
    body = RichTextField()

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "footer footer"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Footer Text"
