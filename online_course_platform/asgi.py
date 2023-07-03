"""
ASGI config for online_course_platform project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import asyncio
import os
import json

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.db import database_sync_to_async
from online_course_platform.urls import websocket_urlpatterns
from django.urls import re_path
from channels.http import AsgiHandler


from online_course_platform.settings import ALL_COINS
from currency.models import Currency
from currency.handlers.parser import get_crypto_rank

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_course_platform.settings')
django_asgi_app = get_asgi_application()


async def application(scope, receive, send):
    if scope['type'] == 'http':
        await django_asgi_app(scope, receive, send)
    elif scope['type'] == 'websocket':
        await websocket_application(scope, receive, send)
        

async def websocket_application(scope, receive, send):
    
    await send({
        'type': 'websocket.accept'
    })
    
    while True:
        message = await receive()
        
        if message['type'] == 'websocket.receive':
            text = message['text']
            
            
            response = {
                'type': 'websocket.send',
                'text': json.dumps(get_crypto_rank(ALL_COINS))
            }
            
            await send(response)
        
        elif message['type'] == 'websocket.disconnect':
            break 
    
    quotes = await database_sync_to_async(Currency.objects.all)()


if os.environ.get('DJANGO_ENV') == 'development':
    application = AsgiHandler(application)