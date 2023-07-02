from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view(), name="home"),
    #authentication to be handled here
    path("login/", views.login_view(), name="login"),
    path("logout/", views.logout_view(), name="logout"),
    #--normal sign-up and referral based signup here
    path("signup/", views.signup_view(), name= "signup"),
    path("signup/<str: referral_code>/", views.refer_view(), name="referral"),
    #Wallet page
    path("portfolio/", views.portfolio_view(), name="portfolio"),
    #CRUD operations on portfolio
    path("search/", views.search_view(), name="search"),
    path("porfolio_addition", views.portfolio_add(), name= "port_add"), #to add crypto to portfolio
    path("portfolio_deletion", views.portfolio_delete(), name="port_delete"), #to delete a crypto from portfolio
    #password reset
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="reset/password_reset.html"), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name="reset/password_reset_done.html"), name="password_reset_done"),
    path("password_reset_confirm/", auth_views.PasswordResetConfirmView.as_view(template_name="reset/password_reset_confirm.html"), name="password_reset_confirm")
]