import tkinter as tk
import tkinter.messagebox
import configparser
import threading
import queue
import base64
import os
from tkinter.filedialog import askopenfilenames
from datetime import datetime
from main import auto_sender

CONFIG_PATH = os.environ['HOME'] + '/kindler.conf'


class Application:
    def __init__(self, width=363, height=175):
        self.msg_queue = queue.Queue()
        self.w = width
        self.h = height
        self.root = tk.Tk()
        self.root.title('Kindle EBook Sender')
        self.root.protocol('WM_DELETE_WINDOW', lambda: self.root.quit())

    def loop(self):
        self.pack_components()
        self.center_window()
        self.raise_above_all()
        self.root.resizable(False, False)
        self.read_config()
        self.root.mainloop()

    def raise_above_all(self):
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)

    def center_window(self):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = int((ws / 2) - (self.w / 2))
        y = int((hs / 2) - (self.h / 2))
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))

    def pack_components(self):
        row = 0
        subject = 'Kindle Documents ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tk.Label(self.root, text='邮件主题:').grid(row=row, column=0)
        self.email_subject = tk.Entry(self.root)
        self.email_subject.grid(row=row, column=1)
        self.email_subject.insert(0, subject)

        row += 1
        tk.Label(self.root, text='发送邮箱:').grid(row=row, column=0)
        self.send_email = tk.Entry(self.root)
        self.send_email.grid(row=row, column=1)

        row += 1
        tk.Label(self.root, text='密码:').grid(row=row, column=0)
        self.user_password = tk.Entry(self.root, show="*")
        self.user_password.grid(row=row, column=1)

        row += 1
        tk.Label(self.root, text='接收邮箱:').grid(row=row, column=0)
        self.receive_email = tk.Entry(self.root)
        self.receive_email.grid(row=row, column=1)

        row += 1
        tk.Label(self.root, text='电子书路径:').grid(row=row, column=0)
        self.dir_entry = tk.Entry(self.root)
        self.dir_entry.grid(row=row, column=1)
        tk.Button(self.root, text='选择电子书', command=self.select_path_event).grid(row=row, column=2)

        row += 1
        self.send_button = tk.Button(self.root, text='发送附件', command=self.send_event)
        self.send_button.grid(row=row, column=1)

    def select_path_event(self):
        file_list = askopenfilenames()
        path_str = ','.join(file_list)
        self.dir_entry.insert(0, path_str)

    def send_event(self):
        self.change_btn_state()
        auto_sender.subject = self.email_subject.get()
        send_email = self.send_email.get()
        account_list = send_email.split('@')
        if len(account_list) == 0:
            tk.messagebox.showinfo('提示', '邮件账户错误')
            return
        try:
            self.smtp_sender = auto_sender.SmtpSender(main_host='smtp.' + account_list[1],
                                                      main_user=account_list[0],
                                                      main_password=self.user_password.get(),
                                                      sender=send_email,
                                                      receivers=self.receive_email.get(),
                                                      subject=self.email_subject.get(),
                                                      e_boot_file_list=self.dir_entry.get().split(','))
        except Exception as e:
            print(e.args)
            self.show_error_msg()
            return

        send_thread = threading.Thread(target=self.smtp_sender.send_attachment, kwargs={'queue': self.msg_queue})
        send_thread.start()
        send_thread.join()
        self.root.after(100, self.listen_for_result())

    def show_success_msg(self):
        tk.messagebox.showinfo('提示', '推送成功')
        self.change_btn_state()
        self.write_config()

    def show_error_msg(self):
        tk.messagebox.showinfo('提示', '推送失败')
        self.change_btn_state()
        self.write_config()

    def change_btn_state(self):
        if self.send_button['state'] == tk.DISABLED:
            self.send_button['state'] = tk.NORMAL
        else:
            self.send_button['state'] = tk.DISABLED

    # 接收queue message
    def listen_for_result(self):
        if self.msg_queue.qsize() <= 0:
            self.root.after(100, self.listen_for_result())
        else:
            msg = self.msg_queue.get(0)
            if msg is 'success':
                self.show_success_msg()
            else:
                self.show_error_msg()

    def read_config(self):

        if not os.path.exists(CONFIG_PATH):
            fp = open(CONFIG_PATH, 'w')
            fp.close()

        sender = ''
        password = ''
        receivers = ''
        config = configparser.ConfigParser()
        try:
            config.read(CONFIG_PATH)
            main_password = config.get('smtp', 'main_password')
            sender = config.get('smtp', 'sender')
            receivers = config.get('smtp', 'receivers')
            password = base64.b64decode(main_password).decode('utf-8')
        except Exception as e:
            print(e.args)
            pass
        self.send_email.insert(0, sender)
        self.user_password.insert(0, password)
        self.receive_email.insert(0, receivers)

    def write_config(self):
        config = configparser.ConfigParser()
        config.add_section('smtp')
        password = self.smtp_sender.main_password
        encrypt_password = base64.b64encode(password.encode('utf-8'))
        config.set('smtp', 'main_password', encrypt_password.decode('utf-8'))
        config.set('smtp', 'sender', self.smtp_sender.sender)
        config.set('smtp', 'receivers', self.smtp_sender.receivers)
        config.write(open(CONFIG_PATH, 'w'))


app = Application()
app.loop()
