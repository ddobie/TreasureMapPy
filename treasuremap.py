import requests
import urllib.parse
import os
import sys
import json
import logging

class Pointings:
    '''
    Store all pointing information for submission to treasuremap

    :param status: Observing status, either `planned` or `completed`
    :type status: str
    :param graceid: Event ID in GraceDB
    :type graceid: str
    :param instrumentid: Instrument ID
    :type instrumentid: int
    :param band: Observing band
    :type band: str
    :param api_token: Treasuremap API token, defaults to None
    :type api_token: str
    '''

    def __init__(self, status, graceid, instrumentid, band, api_token=None):
        '''Constructor method
        '''
        
        self.logger = logging.getLogger('treasuremap.Pointings')
        
        self.BASE = 'http://treasuremap.space/api/v0'

        assert status in ["planned", "completed"],"Status must be planned or completed"

        self.status = status
        self.graceid = graceid
        self.band = band
        self.instrumentid = instrumentid
        
        if api_token is None:
            self.api_token = os.getenv('TREASUREMAP_API')
        else:
            self.api_token = api_token
        
        self.pointings = []

    def add_pointing(self, ra, dec, time, depth,
                     depth_unit, pos_angle=0.0):
        '''
        Add pointing

        :param ra: Right Ascension of pointing centre
        :type ra:
        :param dec: Declination of pointing centre
        :type dec:
        :param time: Observation time
        :type time: str, formatted as 'YYYY-MM-DDTHH:MM:SS.FF'
        :param depth: Pointing depth (5 sigma image RMS)
        :type depth: float
        :param depth_unit: Depth unit
        :type depth_unit: str
        :param pos_angle: Pointing position angle, defaults to 0.0
        :type pos_angle: float, optional
        '''

        pointing = {
            "status": self.status,
            "position": "POINT({} {})".format(ra, dec),
            "instrumentid": self.instrumentid,
            "pos_angle": pos_angle,
            "time": time,
            "band": self.band,
            "depth": depth,
            "depth_unit": depth_unit
        }

        self.pointings.append(pointing)

    def build_json(self):
        '''
        Build the json data
        '''

        self.json_data = {
            "graceid": self.graceid,
            "api_token": self.api_token,
            "pointings": self.pointings
        }

    def submit(self):
        '''
        Submit pointings to treasuremap
        '''
        TARGET = 'pointings'
        url = '{}/{}'.format(self.BASE, TARGET)
        r = requests.post(url=url, json=self.json_data)

        return r
        
    def cancel(self, ids):
        '''
        Cancel individual pointings
        
        :param ids: list of treasuremap pointing IDs
        :type ids: list
        '''
        
        TARGET = "updated_pointings"
        
        if self.status != "planned":
            logger.critical("Can only cancel planned pointings")
            return
        
        params = {
            "api_token":self.api_token,
            "ids":ids,
            "status":"cancelled"
        }
        
        url = "{}/{}?{}".format(self.BASE, self.TARGET, urllib.parse.urlencode(params))
        
        r = requests.post(url = url)
        
        return r
        
        
    def cancel(self):
        '''
        Cancel all pointings for an event
        '''
        
        TARGET = "cancel_all"
        
        if self.status != "planned":
            logger.critical("Can only cancel planned pointings")
            return
        
        params = {
            "api_token":self.api_token,
            "ids":ids,
            "status":self.instrument
        }
        
        url = "{}/{}?{}".format(self.BASE, self.TARGET, urllib.parse.urlencode(params))
        
        r = requests.post(url = url)
        
        return r
