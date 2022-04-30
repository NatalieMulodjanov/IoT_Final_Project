import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
import easyimap as imap

def sendEmail(subject):

    #print("test 1")

    sender_email = "mankirattest@gmail.com"
    receiver_email = "mankirattest@gmail.com"
    password = "mankirat1"

    #print("test 2")

    # message = MIMEMultipart("alternative")
    # message["Subject"] = "Light is under 400!"
    # message["From"] = sender_email
    # message["To"] = receiver_email

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    #print("Test 3")

    # Create the plain-text and HTML version of your message

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(subject, "plain")

    #print("Test 4")


    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    #print("Test 5")

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    #print("Test 8")

def receive_email():
    server = imap.connect("imap.gmail.com", "mankirattest@gmail.com", "mankirat1")
    server.change_mailbox("Inbox")
    server.listids()
    email = server.mail(server.listids()[0])
    return email.body.strip()[0:3].lower() == 'yes'