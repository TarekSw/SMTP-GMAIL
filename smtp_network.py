#Tarek Swaidane - 201701409 - ths001@pu.edu.lb

#First thing to do:
# - Got to the google account settings and turn On Less Secure Apps feature.
# in order to be able to send email from an outside application using the SMTP server.

#used the create the email object message in order to send it.
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

#used to show dialog box in case of success or failers
from tkinter import messagebox

#Used to create the GUI
import tkinter as thinker

#used for establishing an server SMTP connection
import smtplib

#used for checking the regular expression comparisoon
import re

#regular expression to check if the gmail entered is valid or not.
reg = '^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$'

# the main function through where the email is sent and the SMTP connection is established
def mail(sender_address, sender_password, recipient_address, subject, body):
    try:
        #Taking the data for the email and save them into 
        #message object instantiated from MIMEMultipart object. 
        #where save multiple headers into 1 object as a message format.
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = sender_password
        message['Subject'] = subject

        #attach the body taken from the UI into the message object as  plain text.
        message.attach(MIMEText(body, 'plain'))
        
        #convert that object into plain text (String) in order
        # to be able to send it through the email
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
        messagebox.showinfo("Successfull", "Your Email Was Sent Successfully")

        #if any error happened for whatever reason it will show a dialog ox
        # saying that an error occurred and also print the error message by using (str(e))    
    except Exception as e:
        messagebox.showerror("Error!",'Error : ' + str(e))


#this function is used foe the sake is when the user clicks on the GUI send the email button it run
#the following code which as shown below takes an event as a parameter. where the event in this case
#is button clicked. after the button clicked it checks if the recipient gmail match the regular 
#expression defined ^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$ and if the regular expression matches 
# the email entered it call the mail function defined previously and passes the required parameters.
#where it takes to sender email and password in order to login into the server and after that it takes to receiver email
# and the email subject & body it send the email to the receiver address taken as a parameter
def send_on_click(event):
    if re.search(reg, str.lower(recipient_text.get())):
         mail(str.lower(sender_text.get()), password_text.get(), str.lower(recipient_text.get()), subject_text.get(), body_text.get("1.0", "end"))
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


#this the code for Graphical User Interface (GUI)
if __name__ == "__main__":
    #CREATE a GUI window in order to put the frames in it. where the window is like a box where
    # you put your frames in. the frames are the text input & buttons & ... that you define and you to put
    # in your GUI.
    #here we defined our window and created our frames which they are the text inputs and the button and wired them up with the code.
     window = thinker.Tk()
     window.title("CMPS245 Project")
     firstFrame = thinker.Frame()
     SecondFrame = thinker.Frame()
     ThirdFrame = thinker.Frame()

     sender_email = thinker.Label(master=firstFrame, text="From:")
     sender_email.pack(side=thinker.LEFT, fill=thinker.BOTH)
     sender_text = thinker.Entry(master=firstFrame)
     sender_text.pack()
     sender_text.bind('<KeyRelease>', text_get)
     firstFrame.pack(padx=10, pady=10)

     sender_password = thinker.Label(master=firstFrame, text="Password:")
     sender_password.pack(side=thinker.LEFT, fill=thinker.BOTH)
     password_text = thinker.Entry(master=firstFrame)
     password_text.pack()
     password_text.bind('<KeyRelease>', text_get)
     firstFrame.pack(padx=10, pady=10)
    
     recipient = thinker.Label(master=firstFrame, text="Recipient:")
     recipient.pack(side=thinker.LEFT, fill=thinker.BOTH)
     recipient_text = thinker.Entry(master=firstFrame)
     recipient_text.pack()
     recipient_text.bind('<KeyRelease>', text_get)
     firstFrame.pack(padx=10, pady=10)
    
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