from django.urls import path

from .views import (
    IndexView, propertyDetailView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('p/<slug:slug>/', propertyDetailView.as_view(), name='property-single'),

]
