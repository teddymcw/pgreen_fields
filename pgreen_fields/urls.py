from django.conf.urls import url
from . import views

urlpatterns = [
    url('home/', views.SolarPanelListView.as_view(), name='home'),
    url('create/', views.SolarPanelCreateView.as_view(), name='create'),

    ]