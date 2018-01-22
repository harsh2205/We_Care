import datetime

from decimal import Decimal

from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from module.models import Appointment_Status, Appointment, Bills, Prescription_List, Prescription_Details, Batch, \
    Bill_status, temp


# Create your views here.


def sendMail(sender,reciver,msg):
    sender = 'support@codeblue.in'
    recipient = 'karan.sheth60@gmail.com'

    # Create message
    msg = MIMEMultipart()
    msg = MIMEText("Message text")
    msg['Subject'] = "Sent from python"
    msg['From'] = sender
    msg['To'] = recipient

    # Create server object with SSL option
    server = smtplib.SMTP_SSL('smtp.zoho.com', 465)

    # Perform operations via server
    server.login('support@codeblue.in', 'dhara007')
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()


def checkStatus():
    pass


def View_Pending_Bills(request):
    x = get_object_or_404(Appointment_Status, status='Billing')
    Biling_Appointments = Appointment.objects.filter(status=x)
    print(Biling_Appointments)

    Context_dictonary = {
        'object': Biling_Appointments,
        'title': "View Pending Bills",
        'xedit': "supplier"

    }
    return render(request, "pharmacy/list_bills.html", Context_dictonary)


def Cancle_Bills(request, id=None):
    x = get_object_or_404(Appointment_Status, status='Completed')
    print()
    App = get_object_or_404(Appointment, id=id)
    App.status = x
    App.save()
    return HttpResponseRedirect("/xpharma/vpb/")


def Mark_as_Paid_Bills(request, id=None):
    x = get_object_or_404(Appointment_Status, status='Completed')
    print()
    App = get_object_or_404(Appointment, id=id)
    Bill = get_object_or_404(Bills,Appointment=App)
    Bill.status = get_object_or_404(Bill_status,status="Paid")
    Presciption_Number = get_object_or_404(Prescription_List, appointment=App)
    Prescription_Object = Prescription_Details.objects.filter(prescription=Presciption_Number)

    flag = 0

    for data in Prescription_Object:
        y = temp.objects.filter(product=data.product).aggregate(Sum('count'))
        print(y['count__sum'])
        bat = data.batch.available_count
        print(bat)
        result = int(bat) - int(y['count__sum'])
        print(result)
        if result <= 0:
            return HttpResponseRedirect("/Error")
        else:
            y = temp()
            y.product = data.product
            y.count = data.quantity
            y.save()
            App.status = x
            App.save()
            Bill.save()
            return HttpResponseRedirect("/xpharma/vpb")


def All_Bills(request):
    # x = get_object_or_404(Appointment_Status,status='Completed')
    # print()

    All_Bill = Bills.objects.all()

    Context_dictonary = {
        'object': All_Bill,
        'title': "View All Bills",
        'xedit': "supplier"
    }

    return render(request, "pharmacy/list_bills_history.html", Context_dictonary)


def Details_Bill(request, id=None):
    App = get_object_or_404(Appointment, id=id)
    Presciption_Number = get_object_or_404(Prescription_List, appointment=App)
    Prescription_Object = Prescription_Details.objects.filter(prescription=Presciption_Number)
    total_amount = 0

    for data in Prescription_Object:
        product = data.product
        power = data.power
        amount = Batch.objects.filter(power=power, product=product).order_by('cost')
        data.batch = amount.first()
        data.amount = amount.first().cost
        total_amount=total_amount+(float(amount.first().cost)*float(data.quantity))
        data.save()

    if not Bills.objects.filter(Appointment=App).exists():
        Bill = Bills()
        Bill.Appointment = App
        Bill.total_amount = (total_amount)+(total_amount*0.08)
        Bill.status = get_object_or_404(Bill_status,status="Pending")
        Bill.save()


    Context_dictonary = {
        'INV': Presciption_Number,
        'date': datetime.date.today().strftime('%b %d, %Y'),
        'object': Prescription_Object,
        'title': "View All Bills",
        'xedit': "supplier"
    }

    return render(request, "pharmacy/details_Bill.html", Context_dictonary)


def Details_Bill_print(request, id=None):
    App = get_object_or_404(Appointment, id=id)
    Presciption_Number = get_object_or_404(Prescription_List, appointment=App)
    Prescription_Object = Prescription_Details.objects.filter(prescription=Presciption_Number)


    Context_dictonary = {
        'INV': Presciption_Number,
        'date': datetime.date.today().strftime('%b %d, %Y'),
        'object': Prescription_Object,
        'title': "View All Bills",
        'xedit': "supplier"
    }

    return render(request, "pharmacy/details_Bill_Print.html", Context_dictonary)
