from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import query
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def contact(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        message = request.POST.get("message")
 
        query.objects.create(
            user=request.user if request.user.is_authenticated else None,
            email=email,
            name=name,
            surname=surname,
            message=message,
        )


        subject = "New Support Query"
        email_message = f"""
        A new support message has been received:
        
        Name : {name} {surname}
        Email: {email}
        Message:
        {message}
        """
        
        admins = User.objects.filter(is_superuser =True)
        
        for admin in admins:
            print(f"Admin:{admin.is_superuser} ", admin)
            send_mail(
                subject,
                email_message,
                '',
                [admin.email],
                fail_silently=False,
            )
            
        user_subject = "We Received Your Support Query"
        user_message = f"""
        Dear {name} {surname},
        
        Thank you for reaching out to our support team. We have received your message and will get back to you as soon as possible.
        
        Here is a summary of your query:
        -------------------------------
        {message}
        
        Best regards,
        Support Team
        """
        
        send_mail(
            user_subject,
            user_message,
            '',  
            [email],                     
            fail_silently=False,
        )
            
        messages.success(request, "Your message has been sent successfully!")
        return redirect("help")
    

    return render(request, "support/contact.html")