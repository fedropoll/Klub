from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from smtplib import SMTPAuthenticationError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, SMTPAuthenticationError):
        return Response(
            {
                'detail': 'Ошибка при отправке email для подтверждения. Пожалуйста, проверьте настройки почты (EMAIL_HOST_USER и EMAIL_PASSWORD) и убедитесь, что вы используете пароль приложений Google.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if response is None:
        return Response(
            {'detail': 'Произошла внутренняя ошибка сервера. Пожалуйста, свяжитесь с администратором.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if response is not None:
        if response.status_code == 400:
            if 'non_field_errors' in response.data:
                response.data = {'detail': response.data['non_field_errors'][0]}
            elif 'doctor' in response.data:
                response.data = {'detail': f"Ошибка в поле 'врач': {response.data.get('doctor', [''])[0]}"}
            elif 'service' in response.data:
                response.data = {'detail': f"Ошибка в поле 'услуга': {response.data.get('service', [''])[0]}"}
            elif 'duration_minutes' in response.data:
                response.data = {'detail': f"Ошибка в данных услуги: {response.data.get('duration_minutes', [''])[0]}"}

        if response.status_code == 500 and response.data == {'detail': 'A server error occurred.'}:
            response.data = {'detail': 'Произошла внутренняя ошибка сервера. Пожалуйста, попробуйте позже.'}

    return response
