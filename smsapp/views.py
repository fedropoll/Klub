from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import SMSSerializer
from decouple import config

TEXTBELT_API_KEY = config('TEXTBELT_API_KEY')

TEXTBELT_API_URL = 'https://textbelt.com/text'

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import SMSSerializer

class SendSMSView(APIView):

    @swagger_auto_schema(
        request_body=SMSSerializer,
        responses={200: openapi.Response('SMS sent')}
    )
    def post(self, request):
        serializer = SMSSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            message = serializer.validated_data['message']

            # Отправка запроса
            response = requests.post(TEXTBELT_API_URL, {
                'phone': phone,
                'message': message,
                'key': TEXTBELT_API_KEY
            })

            result = response.json()

            if result.get('success'):
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
