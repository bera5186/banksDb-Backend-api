from django.urls import path
from .views import BranchSearch, BranchesAutocomplete, BankInfo
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('branches/search/', BranchSearch.as_view()),
    path('branches/autocomplete/', BranchesAutocomplete.as_view()),
    path('banks/<int:id>', BankInfo.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)