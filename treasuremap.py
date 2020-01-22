import requests
import urllib.parse
import os
import sys
import json


class Pointings:
    '''
    Store all pointing information for submission to treasuremap

    :param status: Observing status, either `planned` or `completed`
    :type status: str
    :param graceid: Event ID in GraceDB
    :type graceid: str
    :param api_token: Treasuremap API token, defaults to None
    :type api_token: str
    :param instrumentid: Instrument ID, defaults to 65 (for ASKAP)
    :type instrumentid: int
    :param band: Observing band, defaults to `other`
    :type band: str
    '''

    def __init__(self, status, graceid, api_token=None,
                 instrumentid=65, band='other'):
        '''Constructor method
        '''

        assert status in ["planned", "completed"]

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
                     depth_unit='flux_jy', pos_angle=0.0):
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
        :param depth_unit: Depth unit, defaults to `flux_jy`
        :type depth_unit: str, optional
        :param pos_angle: Pointing position angle, defaults to 0.0
        :type pos_angle: float
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
        BASE = 'http://treasuremap.space/api/v0'
        TARGET = 'pointings'
        r = requests.post(url=BASE + '/' + TARGET, json=self.json_data)

        return r
