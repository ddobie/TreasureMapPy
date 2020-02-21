from treasuremap import Pointings

import astropy.units as u
from astropy.coordinates import SkyCoord
import numpy as np
import json

import datetime as dt

# Set up instrument parameters
graceid = "TEST_EVENT"
instrumentid = 65
band = 'L'
depth_unit = 'flux_jy'

# Set up pointing parameters
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

# Set up depth
rms_vals = np.asarray([35, 39, 39])*u.uJy


ra = S190814bv_coord.ra.deg
dec = S190814bv_coord.dec.deg

# Initialise Pointings class
S190814bv = Pointings("planned", graceid, instrumentid, band)

# Loop over each observation and add to Pointings
for start, dur, rms in zip(obs_start, obs_length, rms_vals):
    start_dt = dt.datetime.strptime(start,"%Y-%m-%dT%H:%M:%S")
    dodgy_delta = dt.datetime.strptime(dur, "%H:%M:%S") - dt.datetime.strptime("00:00:00", "%H:%M:%S")
    
    time = start_dt + dodgy_delta/2
    time_str = dt.datetime.strftime(time, "%Y-%m-%dT%H:%M:%S.%f")[:-4]
    
    S190814bv.add_pointing(ra, dec, time_str, rms.to(u.Jy).value * 5, depth_unit)

# Build the JSON and submit
S190814bv.build_json()
request = S190814bv.submit()
print(request["pointing_ids"])

# Cancel the first pointing
cancel_id = request["pointing_ids"][0]
S190814bv.cancel([cancel_id])

# Cancel all pointings
S190814bv.cancel_all()

