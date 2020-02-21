from treasuremap import Pointings

import astropy.units as u
from astropy.coordinates import SkyCoord

import datetime as dt

target_coord = SkyCoord(
    "05:56:18.5156", "-33:09:10.3965",
    unit=(u.hourangle, u.deg))

obs_start = [
    "2019-08-15T19:34:00",
    "2019-05-11T01:13:29"]

obs_length = [
    "10:01:35",
    "11:31:45",]

rms_vals = [40, 40]


ra = target_coord.ra.deg
dec = target_coord.dec.deg
graceid = "S190510g"

target = Pointings("completed", graceid, band='L')

for start, dur, rms in zip(obs_start, obs_length, rms_vals):
    start_dt = dt.datetime.strptime(start,"%Y-%m-%dT%H:%M:%S")
    dodgy_delta = dt.datetime.strptime(dur, "%H:%M:%S") - dt.datetime.strptime("00:00:00", "%H:%M:%S")
    
    time = start_dt + dodgy_delta/2
    time_str = dt.datetime.strftime(time, "%Y-%m-%dT%H:%M:%S.%f")[:-4]
    
    target.add_pointing(ra, dec, time_str, rms * 5)

target.build_json()
request = target.submit()
print(request.text)
