import string
from random import SystemRandom

from django.utils.text import slugify


def random_letters(k=5):
    return ''.join(SystemRandom().choices(
        string.ascii_lowercase + string.digits,
        k=k,
    ))

#print(random_letters(10))

def slugify_new(text):
    return slugify(text) + '-' + random_letters()