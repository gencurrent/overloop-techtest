from django.shortcuts import render

from techtest.author.models import Author
from techtest.utils.views import (
    ListRetreiveAbstractView,
    SinglePostAbstractView,
    SinglePKInstanceAbstractView
)
from techtest.author.schemas import AuthorSchema

class AuthorView(ListRetreiveAbstractView, SinglePostAbstractView):
    
    model = Author
    model_schema = AuthorSchema

class AuthorPKView(SinglePKInstanceAbstractView):
    model = Author
    model_schema = AuthorSchema