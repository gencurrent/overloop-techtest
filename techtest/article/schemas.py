
from marshmallow import validate
from marshmallow import fields
from marshmallow import Schema
from marshmallow.decorators import post_load
from marshmallow.exceptions import ValidationError

from techtest.article.models import Article
from techtest.author.models import Author
from techtest.region.models import Region
from techtest.region.schemas import RegionSchema


class ArticleSchema(Schema):
    class Meta(object):
        model = Article

    id = fields.Integer()
    title = fields.String(validate=validate.Length(max=255))
    content = fields.String()
    author = fields.Method(
        required=False, serialize="get_author", deserialize="load_author", allow_none=True
    )
    regions = fields.Method(
        required=False, serialize="get_regions", deserialize="load_regions"
    )

    def get_regions(self, article):
        return RegionSchema().dump(article.regions.all(), many=True)

    def load_regions(self, regions):
        return [
            Region.objects.get_or_create(id=region.pop("id", None), defaults=region)[0]
            for region in regions
        ]

    def get_author(self, article):
        from techtest.author.schemas import AuthorSchema
        return AuthorSchema().dump(article.author)

    def load_author(self, author):
        author_id = author.pop("id", None)
        author, _ = Author.objects.get_or_create(id=author_id, **author)
        return author

    @post_load
    def update_or_create(self, data, *args, **kwargs):
        regions = data.pop("regions", None)
        article, _ = Article.objects.update_or_create(
            id=data.pop("id", None), defaults=data
        )
        if isinstance(regions, list):
            article.regions.set(regions)
        return article
