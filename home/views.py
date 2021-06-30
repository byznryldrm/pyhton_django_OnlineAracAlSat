
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.serializers import json

# Create your views here.
import car
from car.models import Car, Category, Images
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile


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
        form = ContactFormu(request.POST)
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
    form = ContactFormu()
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


def car_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                cars = Car.objects.filter(title__icontains=query)
            else:
                cars = Car.objects.filter(title__icontains=query, category_id=catid)
            setting = Setting.objects.get(pk=1)
            context = {'cars': cars,
                       'category': category,
                       'setting': setting}
            return render(request, 'cars_search.html', context)
    return HttpResponseRedirect('/')


def car_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        car = Car.objects.filter(title__icontains=q)
        results = []
        for rs in car:
            car_json = {}
            car_json = rs.title
            results.append(car_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Kullanıcı adı veya şifre hatalı!")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            #otomatik profil oluşturma
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/womanavatar.png"
            data.save()
            messages.success(request, "Hoşgeldiniz... Hesabınız oluşturulmuştur.")
            return HttpResponseRedirect('Sign up')
    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form}
    return render(request, 'signup.html', context)

