import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# source_file_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/attachments'
# destination_file_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/archives/attachments.zip'


class StmpSender:
    def __init__(self, main_host, main_user, main_password, sender, receivers, subject, e_boot_file_list):
        self.main_host = main_host
        self.main_user = main_user
        self.main_password = main_password
        self.sender = sender
        self.receivers = receivers
        self.subject = subject
        self.e_boot_file_list = e_boot_file_list

    def send_attachment(self, queue=None):
        message = MIMEMultipart()
        message['from'] = self.sender
        message['to'] = self.receivers
        message['subject'] = self.subject
        message.attach(
            MIMEText('Kindle document attachment email' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'plain',
                     'utf-8'))

        # for file_path in e_book_file_path_arr:
        #     zip_file(file_path, destination_file_path)

        for file_path in self.e_boot_file_list:
            file_name = file_path.split('/')[-1]
            attachment = MIMEApplication(open(file_path, 'rb').read())
            attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
            message.attach(attachment)
        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(self.main_host, 25)
            smtp_obj.login(self.main_user, self.main_password)
            smtp_obj.sendmail(self.sender, self.receivers, str(message))
            queue.put('success')
            print('发送成功')
            smtp_obj.quit()
        except smtplib.SMTPException as e:
            print(e)
            queue.put('error')
