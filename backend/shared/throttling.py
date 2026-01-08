from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'
    rate = '100/min'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
    rate = '4000/day'
