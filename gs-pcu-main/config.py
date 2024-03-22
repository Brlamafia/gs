port = 4229
debug_mode = True

mysql_host = '45.134.11.133'
mysql_port = 3306
mysql_user = 'root'
mysql_pass = 'S98s35&##$F23'
mysql_db = 'gsrp_server_db'

shoppy_key = 'Chw5O8njfpddSRmtP4LIzXcUlichR5jsrgzuY5Zp8mjEQ53tTG'
shoppy_webook_secret = 'he8aCkqwyDvqzNnI'

# Mercado Pago Credentials
MERCADOPAGO_PUBLIC_KEY = 'TEST-c47dcee4-44f3-42ae-b6a8-cb9a5d37295b'
MERCADOPAGO_ACCESS_TOKEN = 'TEST-628114628809088-092400-b2cf8a819112904765e205e04f9e8d49-1102227974'
MERCADOPAGO_CLIENT_ID = '628114628809088'
MERCADOPAGO_CLIENT_SECRET = 'vwgCZBJWFjzqJKykdD8f2HBKOiXNSi7s'

if not debug_mode:
    MERCADOPAGO_PUBLIC_KEY = 'APP_USR-9dc36b96-0921-4af2-b751-a58414517368'
    MERCADOPAGO_ACCESS_TOKEN = 'APP_USR-628114628809088-092400-1d3dcd6baa58560556bea9ec5997744d-1102227974'