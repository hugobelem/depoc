from rest_framework.throttling import UserRateThrottle


class BurstRateTrottle(UserRateThrottle):
    rate = '10/min'


class SustainedRateThrottle(UserRateThrottle):
    rate = '100/day'
