"""
URL configuration for online_course_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path
from currency.handlers.consumers import CryptoQuotesConsumer


from currency.registration import views as registration
from currency.actions import views as action

websocket_urlpatterns = [
    re_path(r'ws/crypto_quotes_group/$', CryptoQuotesConsumer.as_asgi())
]


urlpatterns = [
    path('', registration.home_view, name='home'),
    path('register/', registration.register, name='register'),
    path('login/', registration.login, name='login'),
    path('logout/', registration.logout, name='logout'),
    #path('home/show_crypto/', action.show_crypto, name='show_crypto'),
    #path('home/add_cryptocurrency/', action.add, name='add_crypto'),
    #path('home/remove_cryptocurrency/', action.remove, name='remove_crypto'),
    #path('home/edit_cryptocurrency/', action.edit, name='edit_crypto'),

]
