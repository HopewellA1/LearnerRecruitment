from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import query
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse


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
            settings.DEFAULT_FROM_EMAIL,  
            [email],                     
            fail_silently=False,
        )
            
        messages.success(request, "Your message has been sent successfully!")
        return redirect("help")
    

    return render(request, "support/Contact.html")

@login_required
def QueryList(request):
    
    queries = query.objects.all()
    total_queries = queries.count()
    unresolved_queries = queries.filter(status="Pending").count()
    pending_queries = query.objects.filter(status="Pending")
    resolved_queries = query.objects.filter(status="Resolved")

    return render(request, "support/QueryList.html", {
        "queries": queries,
        "pending_queries": resolved_queries,
        "resolved_queries": pending_queries,
        "total_queries": total_queries,
        "unresolved_queries": unresolved_queries,
    })
    
    



def response(request, queryId):
    user_query  = get_object_or_404(query, pk=queryId)
  
    if request.method == "POST":
    
        response_message = request.POST.get("response_message")

        if response_message:
            
            subject = "Response to Your Support Query"
            email_message = f"""
            Dear {user_query .name} {user_query .surname},

            Thank you for your patience. Here is our response to your query:

            Your Query:
            -------------------------------
            {user_query .message}

            Our Response:
            -------------------------------
            {response_message}

            If you have further questions, feel free to reach out again.

            Best regards,
            Support Team
            """

           
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,  # Sender's email address
                [user_query .email],         # Recipient's email address
                fail_silently=False,        # Raise error if sending fails
            )

            user_query .status = "Resolved"
            user_query .save()
            
            messages.success(request, "Response sent successfully!")
            return redirect("QueryList")
        else:
            messages.error(request, "Please type a response before sending.")

    return render(request, "support/response.html", {"user_query": user_query})

def total_queries_api(request):
    total_queries = query.objects.count()
    unresolved_queries = query.objects.filter(status="Pending").count()

    return JsonResponse({
        "total_queries": total_queries,
        "unresolved_queries": unresolved_queries,
    })
