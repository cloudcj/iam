from inventory.logs.models.access_log import AccessLog


class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        token = getattr(request, 'auth', None)

        user_id = None
        username = None
        department = None

        if token:
            user_id = token.get('sub')
            username = token.get('username')
            department = token.get('department')

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        browser, os_device = _parse_user_agent(user_agent)

        AccessLog.objects.create(
            user_id=user_id,
            username=username,
            department=department,
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            ip_address=request.META.get('REMOTE_ADDR'),
            browser=browser,
            os_device=os_device,
        )

        return response


def _parse_user_agent(ua_string):
    """
    Basic user agent parsing without external library.
    Returns (browser, os_device).
    """
    if not ua_string:
        return None, None

    browser = None
    os_device = None

    # Browser detection
    if 'Edg/' in ua_string:
        browser = 'Edge'
    elif 'Chrome/' in ua_string and 'Safari/' in ua_string:
        browser = 'Chrome'
    elif 'Firefox/' in ua_string:
        browser = 'Firefox'
    elif 'Safari/' in ua_string:
        browser = 'Safari'
    elif 'MSIE' in ua_string or 'Trident/' in ua_string:
        browser = 'Internet Explorer'
    else:
        browser = 'Other'

    # OS / Device detection
    if 'iPhone' in ua_string or 'iPad' in ua_string:
        os_device = 'iOS'
    elif 'Android' in ua_string:
        os_device = 'Android'
    elif 'Windows' in ua_string:
        os_device = 'Windows'
    elif 'Macintosh' in ua_string:
        os_device = 'macOS'
    elif 'Linux' in ua_string:
        os_device = 'Linux'
    else:
        os_device = 'Other'

    return browser, os_device
