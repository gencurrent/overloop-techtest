from marshmallow import validate
from marshmallow import fields
from marshmallow import Schema
from marshmallow.decorators import post_load

from techtest.author.models import Author


class AuthorSchema(Schema):
    class Meta(object):
        model = Author

    id = fields.Integer()
    first_name = fields.String(required=True, validate=validate.Length(max=40))
    last_name = fields.String(required=True, validate=validate.Length(max=40))

    @post_load
    def update_or_create(self, data, *args, **kwargs):
        region, _ = Author.objects.update_or_create(
            id=data.pop("id", None), defaults=data
        )
        return region
