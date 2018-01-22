from django.contrib import admin

# Register your models here.
from module.models import Patient, Appointment, Manufacturer, Supplier, Product, Batch, PatientHistory, \
    Appointment_Status, Prescription_Details, Prescription_List, Bill_status, Bills, temp

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Manufacturer)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Batch)
admin.site.register(Appointment_Status)
admin.site.register(Prescription_Details)
admin.site.register(Prescription_List)
admin.site.register(Bill_status)
admin.site.register(Bills)
admin.site.register(temp)





