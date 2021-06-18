
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
import car
from car.models import Car, Category, Images
from home.models import Setting, ContactForm, ContactFormMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:5]
    category = Category.objects.all()
    lastcars = Car.objects.all().order_by('-id')[:4]
    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'car': car,
               'sliderdata': sliderdata,
               'lastcars': lastcars}
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'aboutus', 'category': category}
    return render(request, 'aboutus.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'references', 'category': category}
    return render(request, 'references.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get['REMOTE_ADDR']
            data.save()
            messages.success(request, "Mesajınız başarı ile iletildi!")
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactForm()
    context = {'setting': setting, 'form': form, 'category': category}
    return render(request, 'contact.html', context)


def category_cars(request, id, slug):
    category = Category.objects.all()
    categorydata = Car.objects.filter(pk=id)
    cars = Car.objects.filter(category_id=id)
    context = {'cars': cars,
               'category': category,
               'categorydata ': categorydata,
               }
    return render(request, 'cars.html', context)


def car_detail(request,id,slug):
    category = Category.objects.all()
    car = Car.objects.get(pk=id)
    images = Images.objects.filter(car_id=id)
    lastcars = Car.objects.all().order_by('-id')[:4]
    setting = Setting.objects.get(pk=1)
    context = {
        'car': car,
        'category': category,
        'images': images,
        'lastcars': lastcars,
        'setting': setting
        }
    return render(request, 'car_detail.html', context)

