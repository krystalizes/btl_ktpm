from django.urls import path
from . import views

urlpatterns = [
    path("getallbook/", views.get_all_book, name = "getallbook"),
    path("book_regis/", views.book_regis, name = "book_regis"),
    path("book_info/<str:pid>/", views.book_info, name = "book_info"),
    path("book_update/<str:id>/", views.update_book, name = "book_update"),
    path("book_delete/<str:id>/", views.book_delete, name = "book_delete"),
]