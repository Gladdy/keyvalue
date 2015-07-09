import random
import string
from api.models import ApiKey
from ipware.ip import get_ip

def create_api_key(user, request, **kwargs):

    success = False

    if request is not None:
        ip = get_ip(request)
    else:
        ip = None

    while not success:
        try:
            key = ApiKey.objects.create(key=random_string(16), created_ip=ip, user=user, **kwargs)
            success = True
        except Exception:
            pass

def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
