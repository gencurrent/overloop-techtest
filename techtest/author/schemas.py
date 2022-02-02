from django.forms import ValidationError
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
        author_id = data.pop("id", None)
        partial = kwargs["partial"]
        if not partial:
            """ POST method """
            if author_id:
                author = Author.objects.get(
                    id=author_id
                )
            if author:
                raise ValidationError("The Author exists")
            author = Author.objects.create(
                id=author_id,
                first_name=data["first_name"],
                last_name=data["last_name"]
            )
            return author
        else:
            """ Put method """
            author, _ = Author.objects.update_or_create(
                id=data.pop("id", None), defaults=data
            )
            return author
