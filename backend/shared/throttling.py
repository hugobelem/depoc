from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'
    rate = '10/min'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
    rate = '50/day'
