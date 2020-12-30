from django import forms

class OrderForm(forms.Form):
    time = forms.IntegerField(initial=2, label="Время аренды")

class AddCarForm(forms.Form):
    name = forms.CharField(max_length=20, label="Название")
    desc = forms.CharField(max_length=50, label="Описание")
    price = forms.IntegerField(label="Цена")
    color = forms.CharField(label="Цвет")
    image = forms.ImageField(label="Фото")