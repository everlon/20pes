from django.urls import path
from django.contrib.auth import views

from .views import (
    AtivarContaView,
    CustomLoginView,
    PainelView,
    IndexView,
    propertyListView,
    propertyDetailView,
    propertyCatListView,
    propertyNewFormView,
    propertyNewFormViewAuthenticated,
    propertyDeleteView,
    propertyEditView,
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
    path('login/', CustomLoginView.as_view(), name='login'),
    path('sair/', views.LogoutView.as_view(), name='logout'),
    path('minhaarea/', PainelView.as_view(), name='painel'),
    path('imoveis-new/', propertyNewFormViewAuthenticated.as_view(), name='property-new-Auth'),
    path('imoveis-del/<int:pk>/', propertyDeleteView.as_view(), name='property-del'),
    path('imoveis-edit/<int:pk>/', propertyEditView.as_view(), name='property-edit'),
]
