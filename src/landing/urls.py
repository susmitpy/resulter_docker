from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login_page",views.login_page,name="login_page"),
    path("logout_page",views.logout_page,name="logout_page"),

    path('', views.home, name='home'),
    path("mainpage",views.mainpage,name="mainpage"),
    path("mainpage_admin",views.mainpage_admin,name="mainpage_admin"),
    path("mainpage_faculty",views.mainpage_faculty,name="mainpage_faculty"),
    path("mainpage_administration",views.mainpage_administration,name="mainpage_administration"),
    path("ManageUsers",views.ManageUsers.as_view(),name="ManageUsers"),
    path("UserDetails",views.UserDetails.as_view(),name="UserDetails"),
    path("password_reset_complete",views.login_page,name="set_password_complete"),
    path("forgot_password",views.forgot_password,name="forgot_password")

  #  path("password_reset",auth_views.PasswordResetView.as_view(html_email_template_name='registration/password_reset_email.html'))


]
