from django.urls import path, re_path
from . import views


urlpatterns = [
    # public
    path('', views.index_view, name='index'),
    # private
    path('get_suggested_strong_password', views.get_suggested_strong_password, name='get_suggested_strong_password'),
    # auth
    path('login/', views.login_user, name='login'),
    path('register/', views.normal_register, name='normal_register'),
    path('forgot_password/', views.normal_forgot_password, name='normal_forgot_password'),
    path('password_reset_confirm/<uidb64>/<token>', views.password_reset_confirm, name='password_reset_confirm'),
    path('logout/', views.user_logout, name='logout'),
    # verify
    path('send_verify_email/', views.send_verify_mail, name='send_verify_email'),
    path('subscription/', views.subscription, name='subscription'),
    path('subscription_confirm/<uidb64>/<token>', views.subscription_confirm, name='subscription_confirm'),
    path('subscription_cancel_confirm/<uidb64>/<token>', views.subscription_cancel_confirm, name='subscription_cancel_confirm'),
    path('subscription_remove_confirm/<uidb64>/<token>', views.subscription_remove_confirm, name='subscription_remove_confirm'),
    path('account_activate_confirm/<uidb64>/<token>', views.account_activate_confirm, name='account_activate_confirm'),
    # active
    path('active_index/', views.active_index, name='active_index'),
    path('admin_active_index/', views.admin_active_index, name='admin_active_index'),

    path('statements/', views.statements_view, name='statements'),
    # all the above are restricted
    path('machine_book/', views.machine_book, name='machine_book'),
    path('machine_end/', views.machine_end, name='machine_end'),
    path('admin_machine_book/', views.admin_machine_book, name='admin_machine_book'),
    path('user_manage/', views.user_manage, name='user_manage'),
    path('delete_user/', views.delete_user, name='delete_user')
]
