from django.db import models
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Page, Orderable
from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.models import register_snippet
from django import forms
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# Create your models here.


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )


class BlogPage(Page):
    date = models.DateField("post date", blank=True, null=True)
    intro = models.CharField(max_length=200)
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField("blog.Author", null=True, blank=True)
    tag = ClusterTaggableManager(through=BlogPageTag, blank=True)

    def main_image(self):
        gallery = self.gallery_images.first()
        if gallery:
            return gallery.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
        InlinePanel("gallery_images", label="Gallery Images "),
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
                FieldPanel("tag"),
            ],
            heading="Blog Information",
        ),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(
        BlogPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )

    caption = models.CharField(blank=True, max_length=250)

    panels = [FieldPanel("image"), FieldPanel("caption")]


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    author_image = models.ForeignKey(
        "wagtailimages.image",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [FieldPanel("name"), FieldPanel("author_image")]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Authors"


class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context["blogpages"] = blogpages
        return context
