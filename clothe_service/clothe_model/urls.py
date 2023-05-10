from django.urls import path
from . import views

urlpatterns = [
    path("getallclothe/", views.get_all_clothe, name = "getallclothe"),
    path("clothe_regis/", views.clothe_regis, name = "clothe_regis"),
    path("clothe_info/<str:pid>/", views.clothe_info, name = "clothe_info"),
    path("clothe_update/<str:pid>/", views.update_clothe, name = "clothe_update"),
    path("clothe_delete/<str:pid>/", views.clothe_delete, name = "clothe_delete"),
]