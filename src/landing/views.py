import json

from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .decorators import allowed_users

from django.views import View
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.contrib.sites.models import Site
from django.contrib.auth.forms import PasswordResetForm,UserChangeForm

from .forms import EmailFieldForm

def forgot_password(req):
    if req.method == "POST":
        form = EmailFieldForm(req.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                form = PasswordResetForm({'email': email})
                form.is_valid()
                form.save(
                        request= req,
                        from_email="weareresulter@gmail.com",
                            email_template_name='registration/html_password_forget_email.html',
                            html_email_template_name='registration/html_password_forget_email.html')
                messages.info(req,"Check Your Mail")
            else:
                messages.info(req,"User does not exists")
    form = EmailFieldForm()
    return render(req,"landing/forgot_password.html",{"form":form})

@method_decorator(login_required(login_url="login_page"), name='dispatch')
class UserDetails(View):
    def get(self,req):
        user = req.user
        print(user.username)

        return render(req,"landing/user_details.html",{"user":user})

    def post(self,req):
        data = json.loads(req.POST.get("data"))
        user = User.objects.get(pk=data["user"])
        user.first_name = data["fn"]
        user.last_name = data["ln"]

        if user.email == data["email"]:
            user.save()

        else:
            user.email = data["email"]
            user.username = data["email"]
            user.save()

        return redirect("/mainpage")


@method_decorator(login_required(login_url="login_page"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=["admin"]),name="dispatch")
class ManageUsers(View):
    def get(self,req):
        groups = Group.objects.values("name")
        rows = User.objects.exclude(groups__name=None).values("id","username","groups__name","first_name","last_name")
        return render(req,"landing/user_mngt.html",{"groups":groups,"rows":rows})

    def post(self,req):
        op =  req.POST.get("op")
        if op == "add":
            self.add_user(json.loads(req.POST.get("data")),req)
        elif op == "del":
            self.del_user(req.POST.get("id"))
        return JsonResponse({"status":"Success"},status=200)

    def add_user(self,data,req):
        email = data["email"]

        user = User.objects.create(username=email,email=email)
        g = Group.objects.get(name=data["group"])
        user.groups.add(g)
        if g=="admin":
            user.is_staff = True

        user.save()
        current_site = Site.objects.get_current()

        domain = current_site.domain


        form = PasswordResetForm({'email': user.email})
        form.is_valid()
        form.save(
                extra_email_context={"dom":domain},
                request= req,
                from_email="weareresulter@gmail.com",
                    email_template_name='registration/html_password_reset_email.html',
                    html_email_template_name='registration/html_password_reset_email.html')


    def del_user(self,user_id):
        User.objects.get(pk=user_id).delete()

# Create your views here.
def home(req):
    return render(req,"landing/home.html")

@login_required(login_url="login_page")
@allowed_users(allowed_roles=["admin"])
def mainpage_admin(req):
    return render(req,"landing/mainpage_admin.html")

@login_required(login_url="login_page")
@allowed_users(allowed_roles=["admin","faculty"])
def mainpage_faculty(req):
    return render(req,"landing/mainpage_faculty.html")

@login_required(login_url="login_page")
@allowed_users(allowed_roles=["admin","administration"])
def mainpage_administration(req):
    return render(req,"landing/mainpage_administration.html")

@login_required(login_url="login_page")
def mainpage(req):
     if req.user.is_superuser:
        return redirect("mainpage_admin")

     if req.user.groups.exists():
         group = req.user.groups.get().name
     if group == "admin":
         return redirect("mainpage_admin")
     elif group == "faculty":
         return redirect("mainpage_faculty")
     elif group == "administration":
         return redirect("mainpage_administration")


def login_page(req):
    if req.method == "POST":
        un = req.POST.get("username")
        pw = req.POST.get("password")

        user = authenticate(req,username=un,password=pw)
        print(user)
        if user is not None:
            if user.last_login == None:
                login(req,user)
                return redirect("UserDetails")
            login(req,user)
            return redirect("mainpage")
        else:
            messages.info(req,"Username OR Password is Incorrect")


    return render(req,"landing/login.html")


def logout_page(req):
    logout(req)
    return redirect("login_page")
