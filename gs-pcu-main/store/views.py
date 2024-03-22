from dis import code_info
from distutils.log import error
from itertools import product
from flask import Flask, Blueprint, render_template, request, session, url_for, abort, redirect
from flask import current_app as app
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
from utils.database import *
from utils.payment import *
from config import *
from datetime import datetime
from os.path import join, dirname, realpath
import requests
import random
import string

# Init
store = Blueprint('store', __name__)

# MySQL
self_app = Flask('info_views')

# Intialize MySQL
try:
	mysql = MySQL(self_app)
	print(' * [store.views] MySQL started')

except Exception as e:
	print(f' * [store.views] MySQL load failed ({e})')

# Store
@store.route("/store", methods = ['GET', 'POST'])
def index():
	if not session.get('id'):
		session['last_url'] = request.url_rule.endpoint
		return redirect( url_for('auth.sign_in') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `shop_products` WHERE `country` = '{session['country']}' ORDER BY `id` DESC;")
	products = cursor.fetchall()

	if not products:
		session['country'] = 'US'
		cursor.execute(f"SELECT * FROM `shop_products` WHERE `country` = '{session['country']}';")
		products = cursor.fetchall()

	return render_template('/store/index.html', session = session, country = session['country'], products = products)

# Store normal
@store.route("/store/normal", methods = ['GET', 'POST'])
def normal():
	if not session.get('id'):
		session['last_url'] = request.url_rule.endpoint
		return redirect( url_for('auth.sign_in') ), 302

	return render_template('/store/normal.html')

@store.route("/store/normal/<product_id>", methods = ['GET', 'POST'])
def payment_normal(product_id):
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `users` WHERE `id_users` = '{session['id']}';")
	user = cursor.fetchone()
	if user.get('conectado'):
		return render_template('/store/normal.html', error = 'Desconectate del servidor para poder comprar.')

	product_id = int(product_id)
	if product_id == 1:
		if remove_coins(session['id'], 10):
			give_vip(session['id'], 1, 30)
			return render_template('/store/normal.html', success = 'Has comprado VIP Bronze')
		else:
			return render_template('/store/normal.html', error = 'No tienes los GS suficientes.')

	if product_id == 2:
		if remove_coins(session['id'], 15):
			give_vip(session['id'], 2, 30)
			return render_template('/store/normal.html', success = 'Has comprado VIP Silver')
		else:
			return render_template('/store/normal.html', error = 'No tienes los GS suficientes.')

	if product_id == 3:
		if remove_coins(session['id'], 20):
			give_vip(session['id'], 3, 30)
			return render_template('/store/normal.html', success = 'Has comprado VIP Gold')
		else:
			return render_template('/store/normal.html', error = 'No tienes los GS suficientes.')

	return render_template('/store/normal.html', error = 'Ese producto no existe.')

# Change currency
@store.route("/change_currency", methods = ['GET', 'POST'])
def change_currency():
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	if session['dollar_mode']:
		session['country'] = session['original_country']
		session['dollar_mode'] = False
	else:
		session['country'] = 'US'
		session['dollar_mode'] = True

	return redirect( url_for('store.index') ), 302

# Select method
@store.route("/payment_method/<product_id>", methods = ['GET', 'POST'])
def payment_method(product_id):
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `shop_products` WHERE `id` = '{escape_text(product_id)}';")
	product = cursor.fetchone()

	if not product:
		return render_template('/info/error.html', code = 404, info = "Este producto no existe")

	if session['country'] != product['country']:
		return render_template('/info/error.html', code = 403, info = "Este producto no está disponible en tu país")

	if session['country'] == 'AR':
		cursor.execute(f"INSERT INTO `payments` (`product_id`, `method`, `user_id`) VALUES ('{product['id']}', 'Mercado Pago', '{session['id']}');")
		mysql.connection.commit()

		preference_data = {
			"notification_url": f'https://gsroleplay.com/automatic_payment/bfverfbshdvf/{session["id"]}/{product["id"]}/6',
			"items": [
				{
					"title": f"{product['name']}",
					"quantity": 1,
					"unit_price": product['price'],
				}
			]
		}

		preference_response = app.mercadopago_sdk.preference().create(preference_data)
		preference = preference_response["response"]
			
		if app.debug:
			return redirect(preference['sandbox_init_point']), 302

		else:
			return redirect(preference['init_point']), 302
		
		return ''

	return render_template('/store/method.html', product = product, session = session)

# Checkout
@store.route("/checkout/<product_id>/<method_id>", methods = ['GET', 'POST'])
def checkout(product_id, method_id):
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `shop_products` WHERE `id` = '{escape_text(product_id)}';")
	product = cursor.fetchone()

	method_id = int(method_id)

	if not product:
		return render_template('/info/error.html', code = 404, info = "Este producto no existe")

	if session['country'] != product['country']:
		return render_template('/info/error.html', code = 403, info = "Este producto no está disponible en tu país")

	if method_id in automatic_methods:
		json_payload = {
			'product':
			{
				'title': f"{product['name']}",
				'price': product['price'],
				'description': f'Bienvenido al sistema de acreditación automática. Seleccione el método con el que desea pagar, una vez que lo haga, la compra de *"{ product["name"] }"* se acreditará automáticamente.',
				'currency': 'USD',
				'unlisted': True,
				'type': "service",
				'gateways': ['Bitcoin', 'Ethereum', 'PayPal', 'Litecoin', 'Stripe'],
				'quantity':
				{
					'min': 1,
					'max': 1
				},
				'webhook_urls':
				{
					'url': f'https://gsroleplay.com/automatic_payment/bfverfbshdvf/{session["id"]}/{product["id"]}/{method_id}'
				}
			}
		}

		if method_id == 0:
			json_payload['product']['gateways'] = ['PayPal']

		if method_id == 1:
			json_payload['product']['gateways'] = ['Bitcoin']

		if method_id == 2:
			json_payload['product']['gateways'] = ['Ethereum']

		if method_id == 3:
			json_payload['product']['gateways'] = ['Litecoin']

		if method_id == 4:
			json_payload['product']['gateways'] = ['Stripe']

		req = requests.post(
			'https://shoppy.gg/api/v1/pay',
			headers = {
				'Content-Type': 'application/json',
				'Authorization': shoppy_key
			},
			json = json_payload
		).json()

		if not req['status']:
			return render_template('/info/error.html', code = 500, info = '500 Internal Server Error: We are unable to process this payment at this time!')

		return render_template('/store/payment.html', method_info = payment_methods[int(method_id)], method_id = method_id, product = product, shoppy_link = req['details']['urls']['payment']['url'])
	
	return render_template('/store/payment.html', method_info = payment_methods[int(method_id)], method_id = method_id, product = product)

# Confirm payment
@store.route("/start_payment/<product_id>/<method_id>", methods = ['GET', 'POST'])
def start_payment(product_id, method_id):
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `shop_products` WHERE `id` = '{escape_text(product_id)}';")
	product = cursor.fetchone()

	if not product:
		return render_template('/info/error.html', code = 404, info = "Este producto no existe")

	if session['country'] != product['country']:
		return render_template('/info/error.html', code = 403, info = "Este producto no está disponible en tu país")

	cursor.execute(f"INSERT INTO `payments` (`product_id`, `method`, `user_id`) VALUES ('{product['id']}', '{payment_methods[int(method_id)][0]}', '{session['id']}');")
	mysql.connection.commit()

	return redirect( url_for('store.receipts') ), 302

# Receipts list
@store.route("/receipts", methods = ['GET', 'POST'])
@store.route("/receipts/<paid>", methods = ['GET', 'POST'])
def receipts(paid = False):
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `payments`, `shop_products` WHERE `payments`.`user_id` = '{session['id']}' AND `shop_products`.`id` = `payments`.`product_id`;")
	payments = cursor.fetchall()
	for payment in payments:
		payment['start_date'] = payment['start_date'].strftime("%m/%d/%Y %H:%M:%S")

	return render_template('/store/receipts.html', payments = payments, paid = paid)

# Upload
@store.route("/pay/<payment_id>", methods = ['GET', 'POST'])
def pay(payment_id):
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `payments`, `shop_products` WHERE `payments`.`id` = '{escape_text(payment_id)}' AND `shop_products`.`id` = `payments`.`product_id`;")
	payment = cursor.fetchone()
	if not payment:
		return render_template('/info/error.html', code = 404, info = "Este pago no existe")

	if payment['state'] != 0:
		return render_template('/info/error.html', code = 403, info = "Esta factura ya fue pagada")

	if payment['user_id'] != session['id']:
		return render_template('/info/error.html', code = 403, info = "No puedes pagar una factura ajena")

	if request.method == 'GET':
		count = 0
		method_id = 0
		for method in payment_methods:
			if method[0] == payment['method']:
				method_id = count
			count += 1

		return render_template('/store/pay.html', payment = payment, method_info = payment_methods[method_id])

	if request.method == 'POST':
		f = request.files['file']
		f.save(join(dirname(realpath(__file__)), f'/usr/share/nginx/html/gs-pcu/static/payments/{payment_id}.png'))

		cursor.execute(f"UPDATE `payments` SET `state` = '1' WHERE `id` = '{escape_text(payment_id)}';")
		mysql.connection.commit()

		return redirect( url_for('store.receipts', paid = True) ), 302

	return redirect( url_for('store.receipts') ), 302

# Check payment status
@store.route("/payment_status/<payment_id>", methods = ['GET', 'POST'])
def payment_status(payment_id):
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `payments`, `shop_products` WHERE `payments`.`id` = '{escape_text(payment_id)}' AND `shop_products`.`id` = `payments`.`product_id`;")
	payment = cursor.fetchone()
	if not payment:
		return render_template('/info/error.html', code = 404, info = "Este pago no existe")

	if payment['state'] == 0:
		return render_template('/info/error.html', code = 403, info = "Esta factura no fue pagada")

	if payment['user_id'] != session['id']:
		return render_template('/info/error.html', code = 403, info = "No puedes pagar una factura ajena")

	count = 0
	method_id = 0
	for method in payment_methods:
		if method[0] == payment['method']:
			method_id = count
		count += 1

	return render_template('/store/payment_status.html', payment = payment, method_info = payment_methods[method_id])

# Random string
def generate_string(count):
	text = ''
	for i in range(count):
		text += random.choice(string.ascii_letters + string.digits)
	return text

# Generate codes
@store.route("/generate_gifts/<amount>", methods = ['GET', 'POST'])
def generate_gifts(amount):
	if not session['admin'] or not session['id'] in payment_validers:
		return redirect( url_for('admin.index') ), 302
	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	total_codes = []
	codes = ''
	
	for x in range( int(amount) ):
		code = f'{generate_string(4)}-{generate_string(4)}-{generate_string(4)}-{generate_string(4)}'.upper()
		code_type = random.choice([1, 1, 1, 2])
		code_extra = 0
		code_info = ''

		vip_names = [
			'NINGUNO',
			'BRONZE',
			'SILVER',
			'GOLD',
			'DIAMANTE'
		]

		if code_type == 1:
			code_extra = random.randint(1, 10)
			code_info = f'{code_extra} GS'
		
		if code_type == 2:
			code_extra = random.choice([1, 1, 1, 2, 2, 3, 3, 4])
			code_info = f'VIP {vip_names[code_extra]}'

		total_codes.append([code, code_info, x + 1])
		cursor.execute(f"INSERT INTO `gift_codes` (`code`, `type`, `extra`) VALUES ('{code}', '{code_type}', '{code_extra}');")
		mysql.connection.commit()


	codes += f'<h3>HTML Format:</h3><br><b>Códigos de regalo ({amount}):</b><br>'
	for item in total_codes:
		codes += f'{item[2]}. <code>{item[0]}</code> 👉 {item[1]}<br>'

	codes += f'<hr><h3>Discord Format:</h3><br>**Códigos de regalo ({amount}):**<br>'
	for item in total_codes:
		codes += f'{item[2]}. `{item[0]}` 👉 {item[1]}<br>'

	codes += f'<hr><h3>Whatsapp Format:</h3><br>*Códigos de regalo ({amount}):*<br>'
	for item in total_codes:
		codes += f'{item[2]}. ```{item[0]}``` 👉 {item[1]}<br>'

	return codes

# Generate codes
@store.route("/generate_boxes/<amount>/<box_type>", methods = ['GET', 'POST'])
def generate_boxes(amount, box_type):
	if not session['admin'] or not session['id'] in payment_validers:
		return redirect( url_for('admin.index') ), 302
	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	total_codes = []
	codes = ''
	
	for x in range( int(amount) ):
		code = f'{generate_string(4)}-{generate_string(4)}-{generate_string(4)}-{generate_string(4)}'.upper()
		code_type = 100
		code_extra = int(box_type)
		code_info = f'Mystery Box ({boxes_names[code_extra]})'

		total_codes.append([code, code_info, x + 1])
		cursor.execute(f"INSERT INTO `gift_codes` (`code`, `type`, `extra`) VALUES ('{code}', '{code_type}', '{code_extra}');")
		mysql.connection.commit()


	codes += f'<h3>HTML Format:</h3><br><b>Códigos de regalo ({amount}):</b><br>'
	for item in total_codes:
		codes += f'{item[2]}. <code>{item[0]}</code> 👉 {item[1]}<br>'

	codes += f'<hr><h3>Discord Format:</h3><br>**Códigos de regalo ({amount}):**<br>'
	for item in total_codes:
		codes += f'{item[2]}. `{item[0]}` 👉 {item[1]}<br>'

	codes += f'<hr><h3>Whatsapp Format:</h3><br>*Códigos de regalo ({amount}):*<br>'
	for item in total_codes:
		codes += f'{item[2]}. ```{item[0]}``` 👉 {item[1]}<br>'

	return codes

# Redeem code
@store.route("/redeem", methods = ['GET', 'POST'])
def redeem():
	if not session.get('id'):
		session['last_url'] = request.url_rule.endpoint
		return redirect( url_for('auth.sign_in') ), 302

	if request.method == 'POST':
		code = escape_text(request.form['code'].replace(' ', ''))
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

		code_result = redeem_code(session['id'], code)
		if code_result == 'INVALID CODE':
			return render_template('/store/redeem.html', error = 'El código ingresado no existe.')

		if 'REDEEMED' in code_result:
			return render_template('/store/redeem.html', error = f'El código ya fue canjeado por {code_result.split(",")[1]}.')

		cursor.execute(f"SELECT nombre, skin FROM users, usuario_principal WHERE id_users = '{session['id']}' AND usuario_id = '{session['id']}';")
		account = cursor.fetchone()
		return render_template('/store/redeem.html', player = account, redeemed = code_result)

	return render_template('/store/redeem.html')

# Automatic
@store.route("/automatic_payment/bfverfbshdvf/<user_id>/<product_id>/<method_id>", methods = ['GET', 'POST'])
def automatic_payment(user_id, product_id, method_id):
	if method_id == '6':
		if request.json.get('data').get('id'):
			payment_response = app.mercadopago_sdk.payment().get(request.json['data']['id'])
			payment = payment_response["response"]

			if payment['status'] != 'approved':
				return 'ye'
		else:
			return 'naonao'
		
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"INSERT INTO `payments` (`product_id`, `state`, `method`, `user_id`, `start_date`, `end_date`) VALUES ('{product_id}', '2', '{payment_methods[int(method_id)][0]}', '{user_id}', NOW(), NOW());")
	mysql.connection.commit()

	dispatch_product(user_id, product_id)
	return 'ye'