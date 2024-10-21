from django.forms.widgets import PasswordInput
from django.shortcuts import render
from .models import CustomUser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import bcrypt


message = None
# Create your views here.
def index(request):
    return render(request, 'form/index.html', {
        "message":message,
        })

def submit(request):
    if request.method == 'POST':
        data = request.POST

        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        password =  hash_password(data.get("password"))
        dob = data.get("dob")

        new_user = CustomUser(name=name, phone=phone, email=email, password=password, date_of_birth=dob) 
        new_user.save()
        
        return render(request, 'form/submission.html')

def send_email(sender_email, receiver_email, subject, body, api_key):
    message = Mail(
        from_email=sender_email,
        to_emails=receiver_email,
        subject=subject,
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"Email sent successfully! Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
