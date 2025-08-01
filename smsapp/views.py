from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import PhoneSerializer

class SendSMSView(APIView):
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']

            resp = requests.post('https://textbelt.com/text', {
                'phone': phone,
                'message': 'здравствуйте это компания safe.clinic это консультация с ботом Алиса',
                'key': 'textbelt_test'
            })

            result = resp.json()
            return Response(result, status=200 if result.get('success') else 400)
        else:
            return Response(serializer.errors, status=400)
