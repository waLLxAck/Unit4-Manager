import random
import string
from time import time

time_now = int(time())


def generate_random_alphanumeric_string(number_of_characters):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=number_of_characters))
