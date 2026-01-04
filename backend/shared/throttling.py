from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'
    rate = '60/min'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
    rate = '3000/day'
