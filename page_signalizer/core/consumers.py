import json
from channels.generic.websocket import WebsocketConsumer
import asyncio
from scraper_logic.scraper import Page_scraper
from .models import Connection_Spec
from asgiref.sync import async_to_sync
import datetime


class ScrapeConsumer(WebsocketConsumer):

    def connect(self):
        self.scraper_id = self.scope['url_route']['kwargs']['scraper_id']
        self.group_name = 'scraper_%s' % self.scraper_id
        self.scraper = Page_scraper()
        self.is_setuped_scraper = False

        # join new 'group'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            # subscribe to the channel
            self.channel_name
        )
        
        self.accept()

       
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # receive msg from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        do_proceed = text_data_json['do_proceed']

        if not self.is_setuped_scraper:
            template_id = text_data_json['template_id']
            connection_specs = Connection_Spec.objects.get(id=template_id)
            self.scraper.set_parameters(connection_specs)
            self.is_setuped_scraper = True

        # send message to channel
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
            'type': 'mode_update',
            'do_proceed': do_proceed,
            }
        )

        
    def mode_update(self, event):
        
        do_proceed = event['do_proceed']
        if do_proceed:
            results = self.scraper.init_signalizer()
            self.send(text_data=json.dumps({
            'is_success': results['IS_SUCCESS'],
            'msg': results['MSG'],
            'timestamp': results['TIMESTAMP'],
            'url': results['URL'],
            }))
        else:
            results = '...'
            self.send(text_data=json.dumps({
                'msg': results,
                'timestamp': datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y %H:%M:%S')
            }))

        
