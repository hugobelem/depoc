from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'business'
    rate = '20/min'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'business'
    rate = '100/day'
