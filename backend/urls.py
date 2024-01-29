from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_model", views.get_model, name="get_model"),
    path("get_model_shap_e", views.get_model_shap_e, name="get_model_shap_e"),
]