import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email

def sendEmail(subject):
    sender_email = "nataliemulodjanov@gmail.com"
    receiver_email = "nataliemulodjanov@gmail.com"
    password = "Canada01"

    # message = MIMEMultipart("alternative")
    # message["Subject"] = "Light is under 400!"
    # message["From"] = sender_email
    # message["To"] = receiver_email

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(subject, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def receive_email():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('nataliemulodjanov@gmail.com', 'Canada01')
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox") # connect to inbox.
    result, data = mail.search(None, "ALL")

    mail_ids = []
    for block in data:
        mail_ids += block.split()
    
    status, data = mail.fetch(mail_ids[mail_ids.__len__() - 1], '(RFC822)')
    for response_part in data:
        # so if its a tuple...
        if isinstance(response_part, tuple):
            message = email.message_from_bytes(response_part[1])

            mail_from = message['from']
            mail_subject = message['subject']

            # then for the text we have a little more work to do
            # because it can be in plain text or multipart
            # if its not plain text we need to separate the message
            # from its annexes to get the text
            if message.is_multipart():
                mail_content = ''

                # on multipart we have the text message and
                # another things like annex, and html version
                # of the message, in that case we loop through
                # the email payload
                for part in message.get_payload():
                    # if the content type is text/plain
                    # we extract it
                    if part.get_content_type() == 'text/plain':
                        mail_content += part.get_payload()
            else:
                # if the message isn't multipart, just extract it
                mail_content = message.get_payload()

            # and then let's show its result
            return {"From": mail_from, "Subject": mail_subject, "Content": mail_content}
