from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = 'user'
    rate = '10/min'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'user'
    rate = '50/day'
