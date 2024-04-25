import os
from flask import Flask
from flask_mail import Mail, Message
import dotenv

# Access the value of an environment variable
dotenv.load_dotenv()
mail_username = os.environ['MAIL_USERNAME']
mail_password = os.environ['MAIL_PASSWORD']

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password

mail = Mail(app)

@app.route('/send-email')
def send_email():
    subject = 'ECO Test Email'
    recipient = 'hgupta@princeton.edu'
    body = 'This is a test email from the ECO Tutoring App.'

    msg = Message(subject=subject, sender=mail_username, recipients=[recipient])
    msg.body = body
    mail.send(msg)

    return 'Email sent successfully!'

if __name__ == '__main__':
    app.run(debug=True)
