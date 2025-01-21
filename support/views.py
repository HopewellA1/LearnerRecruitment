from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import *
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from placement.views import findComps
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


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
    

    return render(request, "support/Contact.html")





#**************************Anouncements********************************************************************
@login_required
def Anouncements(request):
    
    if request.method == 'GET':
        
        
        payload = {
            "anouncements":  getAnouncements(Anouncement.objects.all().order_by('-AnouncementId')),
            "categories": category.objects.all()
        }
        return render(request, 'support/Anouncements.html',payload)
    
    if request.method == 'POST':
        audiance = request.POST["audiance"]
        if( request.POST["CategoryID"] != "None"):
            
            try:
                categ = get_object_or_404(category, pk =int(request.POST["CategoryID"]) )
            except:
                categ = None
        else:
            categ = None
        anouncement = Anouncement.objects.create(
            user = request.user,
            category = categ,
            title = request.POST["subject"],
            description = request.POST["message"],
            audiance = audiance  
        )
        
       
        isent = False
        if audiance =="LearnersCategory": 
            learnersEmails = Learner.objects.filter(category = get_object_or_404(category, pk = int( request.POST["CategoryID"]))).values_list('LearnerEmailAddress', flat=True)
            isent = sendAnouncement(learnersEmails, request.POST["subject"],request.POST["message"], request) 
            pass
        elif audiance == "AllLearners":
            learnersEmails = Learner.objects.all().values_list('LearnerEmailAddress', flat=True)
            isent = sendAnouncement(learnersEmails, request.POST["subject"],request.POST["message"], request)
            pass
        elif audiance == "CompaniesCategory":
            if( request.POST["CategoryID"] != "None"):
                Category = get_object_or_404(category, pk = int( request.POST["CategoryID"]))
                Companies =  findComps(Category)
                CompaniesEmails = getCompaniesEmails(Companies)
                isent = sendAnouncement(CompaniesEmails, request.POST["subject"],request.POST["message"], request)
        elif audiance == "AllCompanies":
            Companies = Company.objects.all() 
            CompaniesEmails = []
            for Comp in Companies:
                CompaniesEmails.append(Comp.user.email)
            isent = sendAnouncement(CompaniesEmails, request.POST["subject"],request.POST["message"], request)
        
        if isent:
            messages.success(request, "Announcement published successfully.")
        else:
            messages.error(request, "Something went wrong while trying to send the announcement please try again or contact support.")
            payload = {
                "anouncements": getAnouncements(Anouncement.objects.all().order_by('-AnouncementId')) ,
                "categories": category.objects.all(),
                "subject": request.POST["subject"],
                "message": request.POST["message"]
                
            }
            return render(request, 'support/Anouncements.html',payload)
            
        return redirect("Anouncements")



def getCompaniesEmails(Companies):
    emails = []
    for company in Companies:
        emails.append(company["Company"].user.email)
    return emails


def sendAnouncement(emails, subject, message, request):
    print("Sent to: ", emails)
    mail_subject =subject
    message = render_to_string("support/alerts/AnouncementEmail.html",{
        'message':message,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    try:
        return send_mail(mail_subject,f"{message}"  ,'',emails, fail_silently=False)
    except:
        return False
    
    
def getAnouncements(anounceList):
    print("We here")
    anouncements= []
    
    for anouncement in anounceList:
        
        anouncements.append({
            "anouncement": anouncement,
            "Sent_to": getSentTo(anouncement.AnouncementId)
        })

    return anouncements


def getSentTo(anouncementId):
    
    try: 
        anouncement = get_object_or_404(Anouncement, pk =anouncementId )
        
        if anouncement.audiance == 'LearnersCategory' or anouncement.audiance == 'AllLearners' :
            return "Learners"
        elif anouncement.audiance == 'CompaniesCategory' or anouncement.audiance == 'AllCompanies':
            return "Companies"
        else:
            return anouncement.audiance
    except:
        return "Unknown"
            
            
    