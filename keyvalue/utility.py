import random
import string
from api.models import Token, Entry
from ipware.ip import get_ip


def create_token(user, request, **kwargs):

    success = False

    if request is not None:
        ip = get_ip(request)
    else:
        ip = None

    while not success:
        try:
            key = Token.objects.create(value=random_string(16), created_ip=ip, user=user, **kwargs)
            success = True
        except Exception:
            pass


def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
