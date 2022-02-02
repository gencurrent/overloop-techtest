import json

from marshmallow import ValidationError, Schema
from django.views.generic import View
from django.db import models

from techtest.utils import json_response

class ListRetreiveAbstractView(View):
    """The abstract class to retrieve a list of model instances values""" 

    model: models.Model = None
    queryset: models.QuerySet = None
    model_schema: Schema = None

    def __init__(self):
        if self.model is None and self.queryset is None:
            raise NotImplementedError("The model and queryset are not defined")
        if self.model_schema is None:
            raise NotImplementedError("The model schema is not defined")

    def get(self, request, *args, **kwargs):
        """Retrieve the list of model instances"""
        qs = self.queryset or self.model.objects.all()
        return json_response(self.model_schema().dump(self.model.objects.all(), many=True))


class SinglePostAbstractView(View):
    """The abstract view class to create a single model instance""" 

    model_schema: Schema = None

    def post(self, request, *args, **kwargs):
        """ Create a single model instance"""
        try:
            instance = self.model_schema().load(json.loads(request.body))
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(self.model_schema().dump(instance), 201)


class SinglePKInstanceAbstractView(View):
    """The abstract view class to work with instances by their primary key"""

    model = models.Model
    model_schema: Schema = None
    
    def dispatch(self, request, pk, *args, **kwargs):
        try:
            self.instance = self.model.objects.get(pk=pk)  # What is to be done with this?
        except self.model.DoesNotExist:
            return json_response({"error": f"No {self.model.__class__.__name__} matches the given query"}, 404)
        self.data = request.body and dict(json.loads(request.body), id=self.instance.id)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return json_response(self.model_schema().dump(self.instance))

    def put(self, request, *args, **kwargs):
        try:
            self.instance = self.model_schema().load(self.data)
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(self.model_schema().dump(self.instance))

    def delete(self, request, *args, **kwargs):
        self.instance.delete()
        return json_response()
