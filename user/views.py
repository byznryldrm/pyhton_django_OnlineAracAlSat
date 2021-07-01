from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from car.models import Category
from content.models import Menu, ContentForm, Content
from home.models import UserProfile, Setting
from user.forms import UserUpdateForm, ProfileUpdateForm


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


@login_required(login_url='/login')
def addcontent(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Content()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.type = form.cleaned_data['type']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()
            messages.success(request, 'İçeriğiniz eklendi.')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'İçerik Form Hatası:' +str(form.errors))
            return HttpResponseRedirect('/user/addcontent')
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        menu = Menu.objects.all()
        form = ContentForm()
        context = {
            'category': category,
            'menu': menu,
            'setting': setting,
            'form': form}
        return render(request, 'user_addcontents.html', context)


@login_required(login_url='/login')
def contentedit(request,id):
    content = Content.objects.get(id=id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'İçeriğiniz güncellendi.')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'İçerik Form Hatası:' +str(form.errors))
            return HttpResponseRedirect('/user/contentedit/' +str(id))
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        menu = Menu.objects.all()
        form = ContentForm(instance=content)
        context = {
            'category': category,
            'menu': menu,
            'setting': setting,
            'form': form}
        return render(request, 'user_addcontents.html', context)


@login_required(login_url='/login')
def contentdelete(request,id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'İçeriğik silindi.')
    return HttpResponseRedirect('/user/contents')

@login_required(login_url='/login')
def contents(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    menu = Menu.objects.all()
    current_user = request.user
    contents = Content.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'contents': contents,
               'setting': setting,
               'menu': menu}
    return render(request, 'user_contents.html', context)