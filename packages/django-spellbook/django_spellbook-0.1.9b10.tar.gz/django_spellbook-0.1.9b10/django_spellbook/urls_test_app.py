from django.urls import path
from django_spellbook.views_test_app import *

urlpatterns = [
    path('subfolder/test', subfolder_test, name='test_app_subfolder_test')
]