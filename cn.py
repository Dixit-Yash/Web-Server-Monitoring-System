import requests
import tkinter as tk
import threading
import time


class WebServerMonitor:
    def __init__(self, url):
        self.url = url
        self.is_running = False
        self.window = tk.Tk()
        self.window.title('Web Server Monitor')
        self.window.geometry('1080x400')
        self.window.configure(bg='lightyellow')

        self.url_label = tk.Label(
            self.window, text='Web Server URL:', bg='lightblue', fg='black', font=('Helvetica', 14))
        self.url_label.pack(pady=10)

        self.url_entry = tk.Entry(self.window, width=50)
        self.url_entry.pack()
        self.url_entry.insert(0, url)

        self.status_label = tk.Label(self.window, text='Monitoring...', bg='lightblue', fg='black',
                                     font=('Times New Roman', 20))
        self.status_label.pack(pady=10)

        self.start_button = tk.Button(
            self.window, text='Start', command=self.start_monitoring, width=20, height=2)
        self.start_button.pack(side='left', padx=30, pady=10, anchor='center')

        self.stop_button = tk.Button(
            self.window, text='Stop', command=self.stop_monitoring, width=20, height=2)
        self.stop_button.pack(side='left', padx=30, pady=10, anchor='center')
        self.stop_button['state'] = 'disabled'



        self.window.protocol('WM_DELETE_WINDOW', self.on_close)

    def start_monitoring(self):
        self.url = self.url_entry.get()
        self.is_running = True
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'normal'
        self.monitor_thread = threading.Thread(target=self.monitor_web_server)
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.is_running = False

    def on_close(self):
        self.is_running = False
        self.window.destroy()

    def monitor_web_server(self):
        while self.is_running:
            try:
                response = requests.get(self.url)
                if response.status_code == 200:
                    self.status_label.config(
                        text='Web server is up and running', fg='black')
                    with open('output.txt', 'a') as file:
                        file.write('\nWebserver Monitored:  ')
                        file.write(self.url)
                        file.write("\n")
                        file.write('Status: ')
                        file.write(
                            f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Web server is up and running\n")
                        file.write(
                            "________________________________________________________________________________________\n")
                else:
                    self.status_label.config(
                        text='Web server is down', fg='black')
                    with open('output.txt', 'a') as file:
                        file.write('\nWebserver Monitored:  ')
                        file.write(self.url)
                        file.write("\n")
                        file.write('Status: ')
                        file.write(
                            f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Web server is down\n")
                        file.write(
                            "________________________________________________________________________________________\n")
            except Exception as e:
                self.status_label.config(
                    text='Exception: ' + str(e), fg='black')
                with open('output.txt', 'a') as file:
                    file.write('\nWebserver Monitored:  ')
                    file.write(self.url)
                    file.write("\n")
                    file.write('Status: ')
                    file.write(
                        f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Exception: {e}\n")
                    file.write(
                        "________________________________________________________________________________________\n")

            time.sleep(1)

        self.status_label.config(
            text='Monitoring Stopped', bg='lightblue', fg='black')
        self.start_button['state'] = 'normal'
        self.stop_button['state'] = 'disabled'


if __name__ == '__main__':
    url = input('Enter the URL of the web server to monitor: ')
    monitor = WebServerMonitor(url)
    monitor.window.mainloop()