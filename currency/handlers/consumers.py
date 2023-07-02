from channels.generic.websocket import AsyncWebsocketConsumer
from currency.models import Currency


import json


class CryptoQuotesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'crypto_quotes_group'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        if text_data == 'update':
            # Обновление данных о котировках
            await self.send_crypto_quotes()

    async def send_crypto_quotes(self):
        quotes = await self.get_crypto_quotes()
        data = json.dumps(quotes)
        await self.send(text_data=data)

    async def get_crypto_quotes(self):
        quotes = await Currency.objects.all()
        data = []
        for quote in quotes:
            data.append({
                'name': quote.name,
                'price': quote.price,
                'market_cap': quote.market_cup,
                'difference': quote.difference
            })
        return data