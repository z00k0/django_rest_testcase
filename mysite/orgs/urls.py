from django.urls import path

from . import views


urlpatterns = [
    path('clients/', views.ClientListView.as_view()),
    path('bills/', views.BillListView.as_view()),
    path('upload/', views.FileUploadView.as_view()),

]