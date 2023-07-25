from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'

def sendEmail(email:str, id: str):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "My Subject"
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
    sender = {"name":"John Doe","email":"example@example.com"}
    to = [{"email":email,"name":"Jane Doe"}]
    params = {"parameter":"My param value","subject":"New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
