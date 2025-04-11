from django.urls import path
from django_spellbook.views_docs import *

urlpatterns = [
    path('intro/', intro, name='docs_intro')
]