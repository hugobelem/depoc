from rest_framework.throttling import UserRateThrottle


class BurstRateTrottle(UserRateThrottle):
    rate = '60/min'


class SustainedRateThrottle(UserRateThrottle):
    rate = '500/day'
