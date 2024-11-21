from django.urls import path
from .views import hello_world, TextDataView, GenerateCaptchaView, ValidateCaptchaView

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('text/', TextDataView.as_view(), name='text-data'),
    path('generate/', GenerateCaptchaView.as_view(), name='text-data'),
    path('validate/', ValidateCaptchaView.as_view(), name='text-data'),

]