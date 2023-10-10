import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email():
    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # smtp_server_yahoo = 'smtp.mail.yahoo.com'
    # smtp_port_yahoo = 587

    email_address = 'testbev857@gmail.com'  
    email_password = 'u e n i u h z c h j c l n o g i'


    candidates = [
        {"name": "Aneeth", "email": "Aneeth.Manikantan@gmail.com"},
        {"name": "Beven", "email": "bevenrozario.johnson@gmail.com"},
        {"name": "Srujan", "email": "srujanbpgowda333@gmail.com"},
        {"name": "Sumeet", "email": "hande.sumeet38@gmail.com"}
    ]


    subject = "Job Opportunity at Doodle"
    message_body = "Dear {name},\n\nWe are excited to inform you about a job opportunity at Doodle. Please use the username and password given below to login to the Candidate Space and give an online test.\nUSERNAME: FutureDoodler\nPASSWORD: doodler@123\n\nBest regards,\nDoodle INC."

    # Establishing an SMTP connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_address, email_password)


    for candidate in candidates:
        
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = candidate["email"]
        msg['Subject'] = subject

        message = message_body.format(name=candidate["name"])
        msg.attach(MIMEText(message, 'plain'))
        server.sendmail(email_address, candidate["email"], msg.as_string())


    server.quit()

    print("Emails sent successfully! A..B..C")


