from django.db import models
from datetime import datetime, timedelta




# ОВД
class Ovd(models.Model):
    name_abbreviation = models.CharField(max_length=200)
    name_full = models.CharField(max_length=200, default="", blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name_abbreviation


# Подразделения
class Department(models.Model):
    name_abbreviation = models.CharField(max_length=50)
    ovd = models.ManyToManyField(Ovd, verbose_name='ОВД')
    name_full = models.CharField(max_length=500, default="", blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name_full


# Табель
class Timesheet(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    note = models.TextField()
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Номенклатура
class Nomenclature(models.Model):
    number_1 = models.IntegerField(blank=True, verbose_name='Номер 1')
    number_2 = models.IntegerField(blank=True, verbose_name='Номер 2')
    number_3 = models.IntegerField(blank=True, verbose_name='Номер 3')
    name = models.CharField(max_length=500, verbose_name='Название')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Подразделение')
    note = models.TextField(verbose_name='Описание')
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Положеность
class NecessaryQuantity(models.Model):
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE)
    ovd = models.ForeignKey(Ovd, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.CASCADE)
    number = models.IntegerField()
    isActive = models.BooleanField(default=True)


# Профиль устройства
class DeviceProfile(models.Model):
    name = models.CharField(max_length=500)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Параметры для профиля устройства
class DeviceProfileField(models.Model):
    device_profile = models.ForeignKey(DeviceProfile, on_delete=models.CASCADE,  related_name="fields")
    name = models.CharField(max_length=500)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Статус устройства
class DeviceStatus(models.Model):
    STATUS_DEVICE = [
        ('UNALLOCATED', 'Не распределён'),
        ('NOT_INVENTORY_NUMBER', 'Не присвоен инвентарный номер'),
        ('ALLOCATED', 'Распределен'),
        ('REDISTRIBUTION', 'Перераспределение'),
        ('REDISTRIBUTED', 'Перераспределено'),
        ('REPAIRS', 'Ремонт'),
        ('DEBIT', 'Списан'),
        ('ALLOCATION', 'Распределяется'),
        ('DEVICE_INPUD_DATA', 'Загруженно через файл'),
        ('DEVICE_ADD', 'Добавлен через форму')
    ]
    #name = models.CharField(unique=True, max_length=50, choices=STATUS_DEVICE)
    name = models.CharField(unique=True, max_length=50)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Устройство
class Device(models.Model):
    name = models.CharField(max_length=500)
    serial_number = models.CharField(null=True, blank=True, max_length=500)
    inventory_number = models.CharField(null=True, blank=True, max_length=50)
    status = models.ManyToManyField(DeviceStatus)
    date_input = models.DateTimeField(null=True,
                                      blank=True)  # Дата ввода информации в систему. Используется для формирования отчёта
    price_start_up = models.DecimalField(null=True, blank=True, default=True, max_digits=10, decimal_places=2)
    date_debit = models.DateTimeField(null=True, blank=True)
    provisioner = models.CharField(blank=True, null=True, max_length=500)
    decree = models.CharField(blank=True, null=True, max_length=500)
    delivery_plan = models.CharField(null=True, blank=True, max_length=100)
    invoice = models.CharField(null=True, blank=True, max_length=100)
    date_start = models.DateField(null=True, blank=True, max_length=100)
    date_stop = models.DateTimeField(null=True, blank=True, max_length=100)
    ovd = models.ForeignKey(Ovd, blank=True, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)
    nomenclature = models.ForeignKey(Nomenclature, blank=True, null=True, on_delete=models.CASCADE)
    device_prev = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    device_profile = models.ManyToManyField(DeviceProfile, blank=True)
    note = models.TextField(verbose_name='Описание', default='1')
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Параметры устройства
class DeviceDetail(models.Model):
    device_profile_field = models.ForeignKey(DeviceProfileField, on_delete=models.CASCADE)
    value = models.CharField(max_length=500)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.value


class Report(models.Model):
    TYPE = [
        ('REPORT_DEVICE_PROFILE', 'Отчёт по профилям устройств'),
        ('REPORT_DEVICE_AVAILABLE', 'Отчёт о наличии устройств')
    ]
    name = models.CharField(max_length=500)
    type = models.CharField(max_length=50, choices=TYPE)
    device_profile = models.ManyToManyField(DeviceProfile,blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name

#class ReportDeviceProfile(models.Model):
#    report = models.OneToOneField(Report, on_delete=models.CASCADE, primary_key=True)
#    isActive = models.BooleanField(default=True)

class ReportDeviceProfileDetail(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    device_profile_field= models.ForeignKey(DeviceProfileField,on_delete=models.CASCADE)
    value = models.CharField(max_length=500,null=True)
    isActive = models.BooleanField(default=True)
