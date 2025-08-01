import os
import requests
from twilio.rest import Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_whatsapp_message(to_phone_number, message):
    """
    Отправляет сообщение WhatsApp через Twilio.
    to_phone_number: Номер телефона получателя в формате 'whatsapp:+<код_страны><номер>'
    message: Текст сообщения.
    """
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_whatsapp_number = settings.TWILIO_WHATSAPP_NUMBER

    if not all([account_sid, auth_token, twilio_whatsapp_number]):
        logger.error("Twilio WhatsApp credentials are not fully configured.")
        return False, "Twilio WhatsApp credentials missing."

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            from_=twilio_whatsapp_number,
            body=message,
            to=to_phone_number
        )
        logger.info(f"WhatsApp message sent to {to_phone_number}. SID: {message.sid}")
        return True, "Сообщение WhatsApp успешно отправлено."
    except Exception as e:
        logger.error(f"Error sending WhatsApp message to {to_phone_number}: {e}")
        return False, f"Ошибка отправки сообщения WhatsApp: {e}"

def send_sms_message(to_phone_number, message):
    """
    Отправляет обычное SMS-сообщение через Twilio.
    to_phone_number: Номер телефона получателя в формате E.164 (например, '+77011234567').
    message: Текст сообщения.
    """
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_sms_number = settings.TWILIO_SMS_NUMBER

    if not all([account_sid, auth_token, twilio_sms_number]):
        logger.error("Twilio SMS credentials are not fully configured.")
        return False, "Twilio SMS credentials missing."

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            from_=twilio_sms_number,
            body=message,
            to=to_phone_number
        )
        logger.info(f"SMS message sent to {to_phone_number}. SID: {message.sid}")
        return True, "Сообщение SMS успешно отправлено."
    except Exception as e:
        logger.error(f"Error sending SMS message to {to_phone_number}: {e}")
        return False, f"Ошибка отправки SMS-сообщения: {e}"

def send_telegram_message(chat_id, message):
    """
    Отправляет сообщение Telegram через Telegram Bot API.
    chat_id: ID чата или имя пользователя Telegram (например, '@username').
    message: Текст сообщения.
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        logger.error("Telegram bot token is not configured.")
        return False, "Telegram bot token missing."

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status() # Вызывает исключение для HTTP ошибок (4xx или 5xx)
        logger.info(f"Telegram message sent to chat_id {chat_id}. Response: {response.json()}")
        return True, "Сообщение Telegram успешно отправлено."
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending Telegram message to chat_id {chat_id}: {e}")
        return False, f"Ошибка отправки сообщения Telegram: {e}"
