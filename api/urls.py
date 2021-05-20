from django.urls import path
from .views import BranchSearch, BranchesAutocomplete
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('search/', BranchSearch.as_view()),
    path('autocomplete/', BranchesAutocomplete.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)