from treasuremap import Pointings

import astropy.units as u
from astropy.coordinates import SkyCoord

import datetime as dt

S190814bv_coord = SkyCoord(
    "00:50:37.5", "−25:16:57.371",
    unit=(u.hourangle, u.deg))

obs_start = [
    "2019-08-16T14:10:27",
    "2019-08-23T13:42:59",
    "2019-09-16T12:08:34"]

obs_length = [
    "10:39:25",
    "10:39:01",
    "10:38:42"]

rms_vals = [35, 39, 39]


ra = S190814bv_coord.ra.deg
dec = S190814bv_coord.dec.deg
graceid = "S190814bv"

S190814bv = Pointings("completed", graceid, band='L')

for start, dur, rms in zip(obs_start, obs_length, rms_vals):
    start_dt = dt.datetime.strptime(start,"%Y-%m-%dT%H:%M:%S")
    dodgy_delta = dt.datetime.strptime(dur, "%H:%M:%S") - dt.datetime.strptime("00:00:00", "%H:%M:%S")
    
    time = start_dt + dodgy_delta/2
    time_str = dt.datetime.strftime(time, "%Y-%m-%dT%H:%M:%S.%f")[:-4]
    
    S190814bv.add_pointing(ra, dec, time_str, rms * 5)

S190814bv.build_json()
request = S190814bv.submit()
print(request.text)
