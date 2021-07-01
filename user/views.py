from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from car.models import Category, Car
from home.models import UserProfile, Setting
from user.forms import UserUpdateForm, ProfileUpdateForm, CarAddForm


def index(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'profile': profile,
               'setting': setting,
               }
    return render(request,'user_profile.html',context)


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Hesabınız güncellendi.')
            return redirect('/user')
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'setting': setting,
            'profile_form': profile_form,
            }
        return render(request, 'user_update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifre Başarıyla Değiştirildi')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Lütfen Aşağıdaki Hatayı Düzeltin <br>'+ str (form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form, 'category': category, 'setting': setting}
        )


@login_required(login_url='/login')  # check login
def add_car(request, id):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    url = request.META.get('HTTP_REFERER')
    current_user = request.user  # kullanıcı oturumu bilgilerine erişim
    form = CarAddForm()
    if request.method == 'POST':  # form post edildiyse
        form = CarAddForm(request.POST, request.FILES)
        if form.is_valid():
            data = Car()  # model ile bağlantı
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.category_id = 20
            data.description = form.cleaned_data['description']
            data.price = form.cleaned_data['price']
            data.image = form.cleaned_data['image']
            data.save()  # db kayıt

            messages.success(request, "Your message is saved")
    context = {
        'category': category,
        'form': form,
        'setting': setting,
    }
    return render(request, 'add_car.html', context)


@login_required(login_url='/login')  # check login
def addtreatmenttoadmin(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user  # kullanıcı oturumu bilgilerine erişim
    if request.method == 'POST':  # form post edildiyse
        form = CarAddForm(request.POST)
        if form.is_valid():
            data = Car()  # model ile bağlantı
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.description = form.cleaned_data['description']
            data.price = form.cleaned_data['price']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.slug = form.cleaned_data['slug']
            data.save()  # db kayıt

            messages.success(request, "Your Content Added!")
            url = request.META.get('HTTP_REFERER')  # get last url
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


@login_required(login_url='/login')
def ilanlarim(request):
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    lastcars = Car.objects.all().order_by('-id')[:4]
    context = {'category': category,
               'setting': setting,
               'profile': profile,
               'lastcars': lastcars,
               }
    return render(request, 'ilanlarim.html', context)
