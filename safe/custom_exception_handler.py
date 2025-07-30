from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from smtplib import SMTPAuthenticationError  # Импортируем специфическую ошибку


def custom_exception_handler(exc, context):
    # Вызываем стандартный обработчик исключений DRF, чтобы получить стандартный ответ.
    response = exception_handler(exc, context)

    # Перехватываем специфические ошибки, которые могут привести к 500
    if isinstance(exc, SMTPAuthenticationError):
        # Если это ошибка аутентификации SMTP, возвращаем более конкретное сообщение
        return Response(
            {
                'detail': 'Ошибка при отправке email для подтверждения. Пожалуйста, проверьте настройки почты (EMAIL_HOST_USER и EMAIL_PASSWORD) и убедитесь, что вы используете пароль приложений Google.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Если стандартный обработчик не смог обработать исключение (т.е. это 500 ошибка),
    # или если мы хотим переопределить его поведение для других ошибок.
    if response is None:
        # Это общая 500 ошибка, которую DRF не смог обработать специфически.
        # Возвращаем общее, но более дружелюбное сообщение.
        return Response(
            {'detail': 'Произошла внутренняя ошибка сервера. Пожалуйста, свяжитесь с администратором.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Для всех остальных ошибок, которые были обработаны стандартным обработчиком DRF,
    # возвращаем его ответ.
    return response

