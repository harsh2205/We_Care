import datetime

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings

# Create your models here.


class Patient(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    dob = models.DateField(default="2000-12-21")
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)  # validators should be a list
    blood_group = models.CharField(max_length=3)

    def __str__(self):
        str = self.first_name + " " + self.last_name
        return str

class Appointment_Status(models.Model):
    status = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.status


class Appointment(models.Model):
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="doctor")
    symptoms = models.CharField(max_length=1000)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="data_collected_by")
    date = models.DateField()
    startTime = models.TimeField()
    duration = models.CharField(max_length=10)
    diagnostics = models.CharField(max_length=100000,default="Data")
    status = models.ForeignKey(Appointment_Status, default=1)

    def __str__(self):
        return self.patient.first_name


class Manufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=70)
    location = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.manufacturer_name

    def natural_key(self):
        return self.manufacturer_name


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=70)
    location = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.supplier_name

    def natural_key(self):
        return self.supplier_name, self.location


class Product(models.Model):
    product_name = models.CharField(max_length=70)
    manufacturer = models.ForeignKey(Manufacturer)
    min_req=models.CharField(default=0,max_length=128)

    def __str__(self):
        return self.product_name

    def natural_key(self):
        return self.product_name, self.manufacturer.natural_key(),self.id


class Batch(models.Model):
    product = models.ForeignKey(Product)
    supplier = models.ForeignKey(Supplier)
    count = models.DecimalField(max_digits=10, decimal_places=2)
    available_count = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturing_date = models.DateField()
    expire_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    power = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.product.product_name+"   Supplier: "+self.supplier.supplier_name+"     Purchase Date: "+str(self.purchase_date)

    def natural_key(self):
        return (self.supplier.natural_key(), self.product.natural_key())
    natural_key.dependencies = ['module.Supplier', 'module.Product']


class PatientHistory(models.Model):
    patient = models.ForeignKey(Patient)
    appointment = models.ForeignKey(Appointment)
    prescription = models.CharField(max_length=1000)
    comments = models.CharField(max_length=1000)


class Prescription_List(models.Model):
    appointment = models.ForeignKey(Appointment)




class Prescription_Details(models.Model):
    prescription = models.ForeignKey(Prescription_List)
    product = models.ForeignKey(Product)
    power = models.CharField(max_length=1000)
    quantity = models.CharField(max_length=1000)
    amount = models.CharField(max_length=1000,default=0)
    batch = models.ForeignKey(Batch)

    def __str__(self):
        return self.product.product_name + " -->  " + str(self.prescription.appointment.date)


class Bill_status(models.Model):
    status = models.CharField(default="Pending",max_length=32)

    def __str__(self):
        return self.status


class Bills(models.Model):
    Appointment = models.ForeignKey(Appointment)
    total_amount = models.CharField(default=0,max_length=70)
    time_stemp = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Bill_status)

    def __str__(self):
        return str(self.Appointment)


class temp(models.Model):
    product = models.ForeignKey(Product)
    count = models.CharField(max_length=10000,default=0)
