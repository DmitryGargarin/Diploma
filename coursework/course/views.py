import json
from datetime import time

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm

from django_ajax.decorators import ajax

from .models import Auto, Order
from .forms import OrderForm, AddCarForm

from django.core.serializers import serialize

# Create your views here.
class AjaxHandlerViewIndex(View):
    def __init__(self):
        cars = Auto.objects.all()
        for car in cars:
            car.photo = "images/cars/" + car.photo.url
        return
    def get(self, request):
        text = request.GET.get('button_text')
        result_dict = {}
        cars_json = None
        if request.is_ajax():
            if "убывание" in text:
                result = "Текущая сортировка по цене: возрастание"
                cars = Auto.objects.all().order_by('price')
                # for car in cars:
                #     car.photo = "images/cars/" + car.photo.url
                str_data = serialize('json', cars, cls=DjangoJSONEncoder)
                cars_json = json.loads(str_data)
                for car_num in range(len(cars_json)):
                    car_id = cars[car_num].id
                    result_dict.update({'car' + str(car_num + 1): cars_json[car_num]['fields']})
                    result_dict.update({'car_id' + str(car_num + 1): car_id})
                sort_dict = {'sort': result}
            else:
                result = "Текущая сортировка по цене: убывание"
                cars = Auto.objects.all().order_by('-price')
                # for car in cars:
                #     car.photo = "images/cars/" + car.photo.url
                str_data = serialize('json', cars, cls=DjangoJSONEncoder)
                cars_json = json.loads(str_data)
                for car_num in range(len(cars_json)):
                    car_id = cars[car_num].id
                    result_dict.update({'car' + str(car_num + 1): cars_json[car_num]['fields']})
                    result_dict.update({'car_id' + str(car_num + 1): car_id})
                sort_dict = {'sort': result}
            return JsonResponse(dict(list(result_dict.items()) + list(sort_dict.items())), status=200)
        return render(request, 'index.html')


# def index(request):
#     # sort = "нет"
#     # if sort == "убывание":
#     #     sort = "возрастание"
#     # else:
#     #     sort = "убывание"
#     # cars = Auto.objects.all()
#     # for car in cars:
#     #     car.photo = "images/cars/" + car.photo.url
#     # data = {"cars": cars, "sort": sort}
#     if request.method == 'GET':
#         text = request.GET.get('button_text')
#         # if text == "Сортировка по цене по убыванию":
#         #
#         # cars = Auto.objects.all()
#         # for car in cars:
#         #     car.photo = "images/cars/" + car.photo.url
#         # data = {"cars": cars, "sort": sort}
#         print()
#         print(text)
#         print()
#         return render(request, 'index.html')

def personal(request):
    if request.method == "GET":
        ordered_cars_ids = Order.objects.all().filter(user__exact=request.user.id).values('auto_id')
        ordered_cars = []
        caraddform = AddCarForm()
        for set_id in ordered_cars_ids:
            ordered_cars.append(Auto.objects.get(id__exact=set_id['auto_id']))
        data = {"cars": ordered_cars, "caraddform": caraddform}
        return render(request, "personal.html", context=data)
    if request.method == "POST":
        p = request.POST.get("price", 0)
        n = request.POST.get("name", 0)
        c = request.POST.get("color", 0)
        desc = request.POST.get("desc", 0)
        image = request.POST.get("image", 0)
        car = Auto(name=n, description=desc, photo=image, color=c, price=p)
        car.save()
        return render(request, "personal.html")


def order(request):
    if request.method == "GET":
        car_id = request.GET.get("carid", 0)
        car = Auto.objects.get(id__exact=car_id)
        form = OrderForm()
        data = {"car": car, "form": form}
        return render(request, "order.html", context=data)
    if request.method == "POST":
        time_from_form = request.POST.get("time", 0)
        car_id = request.GET.get("carid", 0)
        curr_user_id = request.user.id
        order = Order(auto_id=car_id, user=curr_user_id, time=time_from_form)
        order.save()
        return HttpResponseRedirect("/")


app_url = "/"


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = app_url + "login/"
    template_name = "reg/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "reg/login.html"
    success_url = app_url

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(app_url)


class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    template_name = 'reg/password_change_form.html'
    success_url = app_url + 'login/'

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(PasswordChangeView, self).form_valid(form)
