import smtplib
from email.message import EmailMessage


class EmailSender:

    email_smtp = 'smtp.gmail.com'

    def __init__(self, exec_name, receiver):
        self.message = EmailMessage()
        self.message['Subject'] = 'Ejecucion software cluster'
        self.message['From'] = 'catcnatest@gmail.com'
        self.message['To'] = receiver
        self.message.set_content('La ejecución de ' + exec_name +
                                 ' ha finalizado. Puede consultar el resultado en la siguiente página web: http://10.100.139.94:8080/testsystem/executions/')

    def send(self):
        """
            Envia el correo electronico de notificacion.

        Args:

        Returns:

        """
        server = smtplib.SMTP(self.email_smtp, '587')
        server.ehlo()
        server.starttls()
        email_password = 'zkstpyjmlezqztdp'
        server.login(self.message['From'], email_password)
        server.send_message(self.message)
        server.quit()
