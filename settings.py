import environ

env = environ.Env()

environ.Env.read_env()

DATABASE_URL = env.str('DATABASE_URL')

HTTP_HOST = env.str('HTTP_HOST')
HTTP_PORT = env.int('HTTP_PORT')

SKYPICKER_BASE_HOST_NAME = env.str('SKYPICKER_BASE_HOST_NAME')
SKYPICKER_CHECK_HOST = env.str('SKYPICKER_CHECK_HOST')
PARTNER_NAME = env.str('PARTNER_NAME')
PRICE_CURRENCY = env.str('PRICE_CURRENCY')