import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askopenfilenames
import threading
import queue
from datetime import datetime
from main import auto_sender as sender


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
        self.debug_test()
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
        self.email_subject.insert(0, subject)
        self.email_subject.grid(row=row, column=1)

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

        sender.subject = self.email_subject.get()
        send_email = self.send_email.get()
        account_list = send_email.split('@')
        if len(account_list) == 0:
            tk.messagebox.showinfo('提示', '邮件账户错误')
            return
        sender.main_host = 'smtp.' + account_list[1]
        sender.main_user = account_list[0]
        sender.main_password = self.user_password.get()
        sender.sender = send_email
        sender.receivers = self.receive_email.get()
        sender.e_book_file_list = self.dir_entry.get().split(',')

        send_thread = threading.Thread(target=sender.send_attachment, kwargs={'queue': self.msg_queue})
        send_thread.start()
        send_thread.join()
        self.root.after(100, self.listen_for_result())

    def show_success_msg(self):
        tk.messagebox.showinfo('提示', '推送成功')
        self.change_btn_state()

    def show_error_msg(self):
        tk.messagebox.showinfo('提示', '推送失败')
        self.change_btn_state()

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

    def debug_test(self):
        self.send_email.insert(0, 'wangshuo159@126.com')
        self.user_password.insert(0, 'sw127198')
        self.receive_email.insert(0, 'wangshuo866_3@kindle.cn')


app = Application()
app.loop()
