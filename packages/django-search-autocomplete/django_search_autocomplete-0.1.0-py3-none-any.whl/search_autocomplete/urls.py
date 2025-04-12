from django.urls import path
from .views import SearchConfigView, GenericSearchView

app_name = 'search_autocomplete'

urlpatterns = [
    path('config/', SearchConfigView.as_view(), name='config'),
    path('search/', GenericSearchView.as_view(), name='search'),
] 