from django.urls import re_path
from . import consumers

websocket_urlpatterns= [
    re_path(r'ws/scrape/(?P<scraper_id>\w+)/$', consumers.ScrapeConsumer.as_asgi())
]