from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType



conf = ConnectionConfig(
    MAIL_USERNAME ="forworkkarpow2000pi@gmail.com",
    MAIL_PASSWORD = "kxzghchjghwzfkhe",
    MAIL_FROM = "forworkkarpow2000pi@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


def sendEmail(email:str, id: str):


    html_content = """
    <!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Donnateatre</title>

    <link
            href="http://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/font-awesome.css"
            rel="stylesheet"  type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Montserrat' rel='stylesheet'>
</head>
<body class=" text-white" style="background-color: rgb(2,12,37);font-family: 'Montserrat',regular;">
<div class="container pt-2 pb-5">
    <img src="logo.png" class="img-fluid" alt="" style="max-width: 50%;margin: auto;display: block;">
</div>
<div class="container mt-5  border "  style="margin: auto auto; width: 80%; background-color: rgb(232,232,232);border-radius: 10px;color: black;text-align: center;">
    <br>
    <div class="px-5 pt-2">
        <h4>ВЫ УСПЕШНО ЗАРЕГИСТРИРОВАЛИСЬ В ВИДЕОСЕРВИСЕ ДОНАТЕАТР!</h4>
        <h4>ОСТАЛСЯ ПОСЛЕДНИЙ ШАГ</h4>
    </div>
    <br>
    <div class="mt-2 ">
        <p>Нажмите на кнопку подтверждения,чтобы <br> завершить создание аккаунта</p>
        <button style="background-color: rgb(3,13,40);color:white;font-size: 20px;padding: 15px 20px;border-radius:10px">
            <a href=\""""+ id + """\" style="text-decoration: none;color:white;">Зарегистрироваться</a>
        </button>
    </div>
    <br>
    <div class="m-4">
        <p>Если вы не регистрировались на сайте, проигнорируйте это письмо, без Вашего подтверждения регистрация завершена не будет</p>
    </div>
</div>
</body>
</html>
    """

    message = MessageSchema(
        subject="Регистрация на платформе Donateatr",
        recipients=[email],
        body=html_content,
        subtype=MessageType.html)

    fm = FastMail(conf)
    fm.send_message(message)
    return













