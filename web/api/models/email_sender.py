import smtplib
from email.message import EmailMessage


class EmailSender:
    """
    Clase para enviar correos electrónicos de notificación.

    Atributos:
        email_smtp (str): Servidor SMTP para el envío de correos electrónicos.
        message (EmailMessage): Mensaje de correo electrónico a enviar.
    """

    email_smtp = 'smtp.gmail.com'

    def __init__(self, exec_name, receiver):
        """
        Inicializa un objeto EmailSender con los datos del mensaje.

        Args:
            exec_name (str): Nombre de la ejecución.
            receiver (str): Dirección de correo electrónico del receptor.
        """
        self.message = EmailMessage()
        self.message['Subject'] = 'Ejecucion software cluster'
        self.message['From'] = 'clusterurjcnoreply@gmail.com'
        self.message['To'] = receiver
        self.message.set_content('La ejecución de ' + exec_name +
                                 ' ha finalizado. Puede consultar el resultado en la siguiente página web: http://10.100.139.94:8080/testsystem/executions/')

    def send(self):
        """
        Envía el correo electrónico de notificación.
        """
        server = smtplib.SMTP(self.email_smtp, '587')
        server.ehlo()
        server.starttls()
        email_password = 'tjxlrghdyjdivrmb'
        server.login(self.message['From'], email_password)
        server.send_message(self.message)
        server.quit()
