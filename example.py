from treasuremap import Pointings

import astropy.units as u
from astropy.coordinates import SkyCoord

S190814bv_coord = SkyCoord(
    "0:50:37.5", "−25:16:57.371",
    unit=(u.hourangle, u.deg))

times = [
    "2019-08-16T14:10:27.0",
    "2019-08-23T13:42:59.0",
    "2019-09-16T12:08:34.0"]

rms_vals = [35, 39, 39]


ra = S190814bv_coord.ra.deg
dec = S190814bv_coord.dec.deg
graceid = "TEST_EVENT"

S190814bv = Pointings("completed", graceid)

for time, rms in zip(times, rms_vals):
    S190814bv.add_pointing(ra, dec, time, rms * 5)

S190814bv.build_json()
request = S190814bv.submit()
print(request.text)
