import json
from channels.generic.websocket import WebsocketConsumer
from scraper_logic.scraper import Page_scraper
from .models import Connection_Spec
from asgiref.sync import async_to_sync
import time
from threading import Thread



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
        self.do_proceed = text_data_json['do_proceed']

        if not self.is_setuped_scraper:
            # setup scraper only once for the current socket
            template_id = text_data_json['template_id']
            self.connection_specs = Connection_Spec.objects.get(id=template_id)
            self.scraper.set_parameters(self.connection_specs)
            self.is_setuped_scraper = True

        if self.do_proceed:
            # precludes from overwritting existing thread when not needed
            t1 = Thread(target=self.send_scraper_message)
            t1.start()


    def send_scraper_message(self):
        # send message to channel
        for _ in range(self.connection_specs.max_cycles):
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                'type': 'mode_update',
                'do_proceed': self.do_proceed,
                }
            )


    def mode_update(self, event):
        # send message to the page (update content)
        if self.do_proceed:
            results = self.scraper.get_scraping_results()
            
            self.send(text_data=json.dumps({
            'is_success': results['IS_SUCCESS'],
            'log_line': results['LOG_LINE'],
            'title': self.connection_specs.title,
            }))

            time.sleep(int(results['DELAY']))

            if results['IS_SUCCESS']:
                self.do_proceed = False
        else:
            pass
        
