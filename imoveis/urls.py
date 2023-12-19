from django.urls import path

from .views import (
    AtivarContaView,
    IndexView,
    propertyListView,
    propertyDetailView,
    propertyCatListView,
    propertyNewFormView,
    aboutView,
    contactView
)

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('sobre/', aboutView.as_view(), name='about'),
    path('contatos/', contactView.as_view(), name='contactus'),
    path('imoveis-cadastro/', propertyNewFormView.as_view(), name='property-new'),
    path('imoveis/', propertyListView.as_view(), name='property-grid'),
    path('imoveis/<slug:slug>', propertyCatListView.as_view(), name='property-categ'),
    path('p/<slug:slug>/', propertyDetailView.as_view(), name='property-single'),
    path('ativar-conta/<int:user_id>/', AtivarContaView.as_view(), name='ativar_conta'),
]
