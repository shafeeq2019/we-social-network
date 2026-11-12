from rest_framework.throttling import AnonRateThrottle


class AuthRateThrottle(AnonRateThrottle):
    # Limits login/signup attempts per IP (rate: DEFAULT_THROTTLE_RATES['auth'])
    scope = 'auth'
