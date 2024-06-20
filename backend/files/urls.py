from django.urls import path

from .views import GenerateSignedURL

urlpatterns = [
    path(
        "generate-signed-url/",
        GenerateSignedURL.as_view(),
        name="generate_signed_url",
    ),
]
