from django.db import models

from techtest.author.models import Author


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    regions = models.ManyToManyField(
        'region.Region', related_name='articles', blank=True
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="article_list"
    )

    def __str__(self):
        return f"<Book id={self.id} : title={self.title}>"
