import os
from datetime import timedelta

from decouple import config
from google.cloud import storage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GenerateSignedURL(APIView):
    def post(self, request):
        file_name = request.data.get("file_name")
        content_type = request.data.get("content_type")

        if not file_name or not content_type:
            return Response(
                {"message": "file_name and content_type are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Debugging prints
        print("Generating signed URL for file:", file_name)
        print("Content type:", content_type)
        print(
            "Using credentials:",
            os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        )

        storage_client = storage.Client.from_service_account_json(
            os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        )
        bucket = storage_client.bucket(config("BUCKET_NAME"))
        blob = bucket.blob(file_name)

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=15),
            method="PUT",
            content_type=content_type,
        )

        return Response({"url": url}, status=status.HTTP_200_OK)
