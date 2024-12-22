from rest_framework.throttling import UserRateThrottle

# The actual throttle limit is functioning at half the defined rate.
class BurstRateThrottle(UserRateThrottle):
    rate = '60/min'


class SustainedRateThrottle(UserRateThrottle):
    rate = '500/day'
