import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication

main_host = ''  # host server
main_user = ''  #
main_password = ''

sender = ''
receivers = ''

message = MIMEMultipart()
message['From'] = sender
message['To'] = receivers

subject = ''
message['Subject'] = Header(subject, 'utf-8')

e_book_file_list = []


# source_file_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/attachments'
# destination_file_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/archives/attachments.zip'


def send_attachment(queue=None):
    # 邮件正文内容
    message.attach(MIMEText('Kindle document attachment email', 'plan', 'utf-8'))

    # for file_path in e_book_file_path_arr:
    #     zip_file(file_path, destination_file_path)

    for file_path in e_book_file_list:
        file_name = file_path.split('/')[-1]
        attachment = MIMEApplication(open(file_path, 'rb').read())
        attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
        message.attach(attachment)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(main_host, 25)
        smtpObj.login(main_user, main_password)
        smtpObj.sendmail(sender, receivers, message.as_string())
        queue.put('success')
        print('发送成功')
    except smtplib.SMTPException as e:
        print(e)
        queue.put('error')
