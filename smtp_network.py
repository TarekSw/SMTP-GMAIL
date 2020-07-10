#First thing to do:
# - Got to the google account settings and turn On Less Secure Apps feature.
# in order to be able to send email from an outside application using the Gmail SMTP server.

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from tkinter import messagebox
import tkinter as thinker
import smtplib

#used for checking the regular expression comparisoon
import re

#regular expression to check if the gmail entered is valid or not.
reg = '^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$'

# the main function through where the email is sent and the SMTP connection is established
def mail(recipient_address, subject, body):
    try:

        sender_address = '' #sender email
        sender_password = '' #sender password

        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = sender_password
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))
        
        text = message.as_string()

        #Open a connection with the Gmail SMTP server on the port 587
        SMTPserver = smtplib.SMTP('smtp.gmail.com', 587)
        #Put the SMTP server connection into a TLS mode
        #StartTLS is a protocol command used to inform the email server that the email client
        #wants to upgrade from an insecure connection to a secure one using TLS or SSL
        SMTPserver.starttls()

        #LogIn into the server using the email and the password
        #credentials of your own google account
        SMTPserver.login(sender_address, sender_password)

        #this is where you send the email, by passing those parameters
        #sender email which he have to enable the less secure app access 
        #of his google account on this following link: https://myaccount.google.com/u/3/lesssecureapps
        SMTPserver.sendmail(sender_address, recipient_address, text)

        #Quit/End the connection with the server
        SMTPserver.quit()

        #if email was sent successfully it will show a dialog box saying that  
        # Your Email Was Sent Successfully
        messagebox.showinfo("Successfull", 'Your Email is Sent Successfully to '+recipient_address)

        #if any error happened for whatever reason it will show a dialog ox
        # saying that an error occurred and also print the error message by using (str(e))    
    except Exception as e:
        messagebox.showerror("Error!",'Error : ' + str(e))


#this function is used foe the sake is when the user clicks on the GUI send the email button it run
#the following code which as shown below takes an event as a parameter. where the event in this case
#is button clicked. after the button clicked it checks if the recipient gmail match the regular 
#expression defined ^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$ and if the regular expression matches 
# the email entered it call the mail function defined previously and passes the required parameters.
def send_on_click(event):
    if re.search(reg, str.lower(recipient_text.get())):
         mail(str.lower(recipient_text.get()), subject_text.get(), body_text.get("1.0", "end"))
    else:
        #if any error occurred while doing the previous process it prints an error.
         messagebox.showerror("Error!!", "Please make sure all your input are in the proper format!")
pass


#this function takes as an event parameters. where if the user enters the recipient address
# it enables the button. you can notice that when you open the UI the send this email button is disabled
#but after entering the recipient email the send this email button will be enabled through this function.
def text_get(event):
    if(re.search(reg, str.lower(recipient_text.get()))):
         send_button['state'] = 'normal'
         send_button.bind('<Button-1>', send_on_click)
    else:
         send_button['state'] = 'disabled'
         send_button.unbind('<Button-1>')
pass


#The Graphical User Interface (GUI)
if __name__ == "__main__":
     window = thinker.Tk()
     window.title("CMPS245 Project")
     firstFrame = thinker.Frame()
     SecondFrame = thinker.Frame()
     ThirdFrame = thinker.Frame()
    
     recipient = thinker.Label(master=firstFrame, text="Recipient:")
     recipient.pack(side=thinker.LEFT, fill=thinker.BOTH)
     recipient_text = thinker.Entry(master=firstFrame)
     recipient_text.pack()
     recipient_text.bind('<KeyRelease>', text_get)
     firstFrame.pack(padx=30, pady=30)
    
     subject = thinker.Label(master=SecondFrame, text="Subject:   ")
     subject.pack(side=thinker.LEFT, fill=thinker.BOTH)
     subject_text = thinker.Entry(master=SecondFrame)
     subject_text.pack()
     SecondFrame.pack(padx=10, pady=10)

     body = thinker.Label(master=ThirdFrame, text="Body:",)
     body.pack(side=thinker.LEFT, fill=thinker.BOTH)
     body_text = thinker.Text(master=ThirdFrame)
     body_text.pack()
     ThirdFrame.pack(padx=10, pady=10)

     send_button = thinker.Button(window, text="Send This Email..", font="bold")
     send_button.pack(pady=5)
     send_button.bind('<Button-1>', send_on_click)

     if recipient_text.get() == "":
         send_button['state'] = "disabled"
         send_button.unbind("<Button-1>")
     window.mainloop()
#End of UI code