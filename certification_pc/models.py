from django.db import models

from mts.models import Ovd, Department


class Address(models.Model):
    address = models.CharField(max_length=500)
    isActive = models.BooleanField(default=True)
    def __str__(self):
        return self.address

class Object(models.Model):
    name = models.CharField(max_length=100)
    ovd = models.ForeignKey(Ovd, on_delete=models.CASCADE)
    department = models.ManyToManyField(Department, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Act(models.Model):
    date = models.DateField(blank=True, default=None)
    number = models.CharField(max_length=20)
    isActive = models.BooleanField(default=True)

class PC(models.Model):
    STATUS = [
        ('IS_APPLY', 'Применяется'),
        ('IS_NOT_APPLY', 'Не применяется'),
        ('PROCESSING', 'Обработка')
    ]
    name = models.CharField(max_length=500)
    serial_number = models.CharField(max_length=500, default="")
    inventory_number = models.CharField(max_length=50, default="")
    isUnknownInventoryNumber = models.BooleanField(default=False)
    price_start_up = models.DecimalField(null=True, blank=True, default=True, max_digits=10, decimal_places=2)
    object = models.ForeignKey(Object,null=True, on_delete=models.CASCADE)
    ovd = models.ForeignKey(Ovd,null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department,null=True, on_delete=models.CASCADE)
    user = models.CharField(blank=True,max_length=100, default="")#Пользователь ПЭВМ
    bailee = models.CharField(blank=True,max_length=100, default="")#Материально ответсвенное лицо
    note = models.TextField(blank=True,default='')
    inventory_number_other = models.CharField(blank=True,max_length=100, default="")
    room = models.CharField(blank=True,max_length=50, default="")
    mac_address = models.CharField(blank=True,max_length=17, default="")
    ip_address = models.GenericIPAddressField(default="")
    host_name = models.CharField(blank=True,max_length=500, default="")
    hard_serial_number = models.CharField(blank=True,max_length=500, default="")
    hard_inventary_number = models.CharField(null=True, blank=True,max_length=500, default=None)
    hard_name = models.CharField(blank=True,max_length=500, default="")
    os = models.CharField(blank=True,max_length=500, default="")
    secret_net_studio_version = models.CharField(blank=True,max_length=100, default="")
    crypto_pro_version = models.CharField(blank=True,max_length=100, default="")
    vipnet_client_version = models.CharField(blank=True,max_length=100, default='')
    kaspersky_version = models.CharField(blank=True,max_length=100, default="")
    isApply = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=STATUS, default=STATUS[1][0])
    date_apply = models.DateField(null=True, blank=True, default=None) #ДатаВремя когда администратор принял значение
    date_edit = models.DateField(null=True, blank=True, default=None) #ДатаВремя редактирования
    date_exclude = models.DateField(blank=True, null=True, default=None)
    act = models.ForeignKey(Act, null=True, blank=True, on_delete=models.CASCADE, default=None)
    isActive = models.BooleanField(default=True)
    def __str__(self):
        return self.name+" "+self.inventory_number

class VipnetType(models.Model):
    name = models.CharField(max_length=100)
    isActive = models.BooleanField(default=True)

class VipNet(models.Model):
    identifier = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    date_create = models.DateField(null=True)
    date_remove = models.DateField(null=True)
    ip_real = models.GenericIPAddressField()
    ip_virtual = models.GenericIPAddressField()
    pc = models.ForeignKey(PC, null=True, on_delete=models.CASCADE)
    vipnet_type = models.ForeignKey(VipnetType, null=True, on_delete=models.CASCADE)
    last_date_locked =models.DateField(null=True, blank=True, default=None)
    isLocked = models.BooleanField(default=False)
    isServices = models.BooleanField(default=False)
    note = models.TextField(default="")
    description = models.TextField(default="")
    isActive = models.BooleanField(default=True)


class LogPcEdit(models.Model):
    mac_address = models.CharField(blank=True,max_length=17)
    data_time = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(default="")
    host_name = models.CharField(blank=True,max_length=500, default="")
    hard_name = models.CharField(blank=True,max_length=500, default="")
    os = models.CharField(blank=True,max_length=500, default="")
    secret_net_studio_version = models.CharField(blank=True,max_length=100, default="")
    crypto_pro_version = models.CharField(blank=True,max_length=100, default="")
    vipnet_client_version = models.CharField(blank=True,max_length=100, default="")
    kaspersky_version = models.CharField(blank=True,max_length=100, default="")
    vipnet_identifier = models.CharField(blank=True, max_length=10, default="")

class Nas(models.Model):
    ip = models.GenericIPAddressField(default="")
    name = models.CharField(blank=True,max_length=500, default="")
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    note = models.TextField(default="")

class LogConnect(models.Model):
    pc = models.ForeignKey(PC, null=True, on_delete=models.CASCADE)
    nas = models.ForeignKey(Nas, null=True, on_delete=models.CASCADE)
    mac_address = models.CharField(blank=True, max_length=17, default="")
    data_time = models.DateTimeField(auto_now=True)