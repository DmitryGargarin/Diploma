from django.db import models


# Create your models here.


# Автомобиль:
# айди, название, описание, фото, цвет, цена
class Auto(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    photo = models.ImageField()
    color = models.CharField(max_length=20)
    price = models.IntegerField()

# Пользователь:
# айди, имя, фамилия, возраст, номер телефона (логин), пароль
# class User(models.Model):
#     name = models.CharField(max_length=20)
#     lasname = models.CharField(max_length=20)
#     age = models.IntegerField()
#     phone = models.CharField(max_length=20)
#     password = models.CharField(max_length=16)

# Заказ:
# айди заказа, айди авто, имя пользователя, фамилия пользователя,
# время заказа в часах
class Order(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    user = models.IntegerField(default=1)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1) #django.db.utils.OperationalError: database is locked
    time = models.IntegerField()



#78909c - серый
#ffa733 - оранжевый