from flask_mail import Message

class MailSender:

    def __init__(self, mail, sender):
        self.mail = mail
        self.sender = sender
    
    def send_email(self, subject = '', recipient = '', body = ''):
        msg = Message(subject = subject, sender = self.sender, recipients = [recipient])
        msg.body = body
        self.mail.send(msg)
        return 'Email sent successfully'
 
    def cancel_appointment(self, appt, canceler, other):
        canceler_email = canceler.get_netid() + "@princeton.edu"
        body = f"Hi {canceler.get_name()},\nYou have successfully canceled your appointment with {other.get_name()} on {appt.get_time().strftime('%A, %B %d')} at {appt.get_time().strftime('%I:%M %p')}.\n\nPrinceton ECO Tutoring App Team"
        self.send_email(subject='Appointment Canceled', recipient=canceler_email, body=body)

        other_email = other.get_netid() + "@princeton.edu"
        body = f"Hi {other.get_name()},\n{canceler.get_name()} has canceled their appointment with you on {appt.get_time().strftime('%A, %B %d')} at {appt.get_time().strftime('%I:%M %p')}.\n\nPrinceton ECO Tutoring App Team"
        self.send_email(subject='Appointment Canceled', recipient=other_email, body=body)

    def book_appointment(self, appt, student, tutor, comments):
        student_email = student.get_netid() + "@princeton.edu"
        body = f"Hi {student.get_name()},\nYou have successfuly booked an appointment with {tutor.get_name()} on {appt.strftime('%A, %B %d')} at {appt.strftime('%I:%M %p')}.\n\nAppointment Comments: {comments}\n\nPrinceton ECO Tutoring App Team"
        self.send_email(subject='Appointment Confirmation', recipient=student_email, body=body)

        tutor_email = tutor.get_netid() + "@princeton.edu"
        body = f"Hi {tutor.get_name()},\n{student.get_name()} has booked an appointment with you on {appt.strftime('%A, %B %d')} at {appt.strftime('%I:%M %p')}.\n\nAppointment Comments: {comments}\n\nPrinceton ECO Tutoring App Team"
        self.send_email(subject='Appointment Confirmation', recipient=tutor_email, body=body)
