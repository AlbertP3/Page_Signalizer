from channels.generic.websocket import AsyncConsumer
import json
from bs4 import BeautifulSoup
import requests
from core.models import Connection_Spec
import datetime
from random import uniform
import time



class Page_scraper():

    def __init__(self):
        self.CYCLES_COUNT = 0
        self.CYCLES_LIMIT = 450
        self.MIN_INTERVAL = 15

    
    def set_parameters(self, connection_specs:Connection_Spec):
        # assign connection specs to variables
        self.url = connection_specs.url
        self.mode = connection_specs.mode
        self.sequence = connection_specs.seq
        self.username = connection_specs.username
        self.password = connection_specs.password
        self.interval_seconds = float(connection_specs.interval_seconds)
        self.msg = connection_specs.msg
        self.rand = float(connection_specs.rand)
        self.eta = connection_specs.eta
        if self.eta is not None:
            self.eta = self.pars_eta_to_datetime(self.eta)


    def pars_eta_to_datetime(self, eta):
        try:
            eta = str(eta).split(':')
            hours = int(eta[0])
            minutes = int(eta[1]) if len(eta) >= 2 else 0
            now = datetime.datetime.today()
            return datetime.datetime(now.year, now.month, now.day, hours, minutes, 0)
        except Exception as e:
            print(f'Error while parsing ETA \n {e}')
            return None
            

    def init_signalizer(self):
        with requests.Session() as session:

            # auth if username and password were provided
            if self.username not in [None,''] and self.password not in [None,'']:
                self.authenticate(session)

            is_matched = False

            # start connections loop - TODO posting to websocket
            # while not is_matched and self.CYCLES_COUNT < self.CYCLES_LIMIT:
            #     self.CYCLES_COUNT+=1
            #     is_matched = self.check_exists(session)
            #     if self.mode == 'not_equal':
            #         is_matched = not is_matched           
            #     if not is_matched:
            #         self.wait_between_connections()
            
            # MVP - returns result of just one search
            is_matched = self.check_exists(session)

            # announce results
            results = self.signalize_results(is_success=is_matched)
            return results


    def signalize_results(self, is_success):
        # returns dict: IS_SUCCESS, TIMESTAMP, MSG, URL
        message_success = self.msg
        message_fail = 'Sequence was never found. Try again.'
        message = message_success if is_success else message_fail
        timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y %H:%M:%S')
        return {'IS_SUCCESS':is_success, 
                'TIMESTAMP':timestamp, 
                'MSG':message, 
                'URL':self.url}


    def wait_between_connections(self):
        
        # Estimated Time of Arrival - modifies wait time in accordance
        # to time delta to the event 
        if self.eta is not None:
            time_now = datetime.datetime.today()
            abs_timedelta_seconds = abs((self.eta - time_now).total_seconds())
            eta_adj = 0.00069*(abs_timedelta_seconds/60)**1.618 + 1
        else:
            eta_adj = 1
        
        # randomizes time between connections
        noise = uniform(-self.rand*self.interval_seconds, self.rand*self.interval_seconds)

        time_wait = self.interval_seconds * eta_adj + noise

        # safety check
        time_wait = max(time_wait, self.MIN_INTERVAL)

        print('ITERATION: {} | WAIT_TIME: {:.2f}'.format(self.CYCLES_COUNT, time_wait))
        time.sleep(time_wait)


    def check_exists(self, session):
        is_found = False
        current_html = self.get_html(session)
        is_found = self.searched_sequence_in_page_content(current_html)
        return is_found


    def searched_sequence_in_page_content(self, html):
        match_found = self.sequence in str(html)
        return match_found


    def authenticate(self, session):
        login_form_url = input('URL with login form: ')
        session.post(login_form_url, auth=(self.username, self.password), allow_redirects=True)


    def get_html(self, session):
        try:
            html = session.get(self.url)
            self.bs = BeautifulSoup(html.text, 'html.parser')
            return self.bs
        except Exception as e:
            print(f'{e} occured. Trying again...')
            time.sleep(self.interval_seconds)
            self.get_html()
