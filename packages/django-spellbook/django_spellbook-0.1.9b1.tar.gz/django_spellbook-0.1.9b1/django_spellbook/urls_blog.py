from django.urls import path
from django_spellbook.views_blog import *

urlpatterns = [
    path('first-post/', first_post, name='blog_first-post')
]