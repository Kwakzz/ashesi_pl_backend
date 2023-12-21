from django.urls import path

from account.views import activate_account, register, sign_in, sign_out, send_activation_email


urlpatterns = [
    path('account/register/', register, name='register'),
    path('account/login/', sign_in, name='sign_in'),
    path('account/logout/', sign_out, name='sign_out'),
    path('account/activate', activate_account, name='activate_account'),
    path('account/send_activation_email/', send_activation_email, name='send_activation_email')
]