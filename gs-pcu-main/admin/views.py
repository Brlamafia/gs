from crypt import methods
from flask import Flask, Blueprint, render_template, request, session, url_for, abort, redirect
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
import textwrap
from utils.database import *
from utils.payment import *
import random
import hashlib
from datetime import datetime

# Init
admin = Blueprint('admin', __name__)

# MySQL
self_app = Flask('info_views')

# Intialize MySQL
try:
	mysql = MySQL(self_app)
	print(' * [admin.views] MySQL started')

except Exception as e:
	print(f' * [admin.views] MySQL load failed ({e})')

# Admin
@admin.route("/admin", methods = ['GET', 'POST'])
def index():
	if not session.get('id'):
		session['last_url'] = request.url_rule.endpoint
		return redirect( url_for('auth.sign_in') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `usuario_principal` WHERE `usuario_id` = '{session['id']}';")
	principal = cursor.fetchone()
	if principal:
		session['admin'] = principal['admin']

	if session['admin'] < 2:
		return 'que andas mirando...'

	return render_template('/admin/index.html')

# Admin registry
@admin.route("/admin/registry", methods = ['GET', 'POST'])
def registry():
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	if session['admin'] < 3:
		return redirect( url_for('admin.index') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT * FROM `admin_registry` ORDER BY `date` DESC LIMIT 500;")
	registry = cursor.fetchall()

	for item in registry:
		item['hidden'] = False

		if item['admin_name'] in ['Josepe_Guebo', 'Konni_Moonlight', 'Big_Benitoo']:
			item['hidden'] = True

	return render_template('/admin/admin_registry.html', registry = registry, session = session)

# Reset user password
@admin.route("/admin/password/reset", methods = ['GET', 'POST'])
def reset_password():
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	permissions = False
	if session['admin'] >= 10:
		permissions = True
	
	if session['id'] == 18703:
		permissions = True

	if not permissions:
		return redirect( url_for('admin.index') ), 302

	if request.method == 'GET':
		return render_template('/admin/reset_password.html')

	if request.method == 'POST':
		add_admin_registration(session['id'], 'Restablecer contraseña', request.form['filter'])

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

		cursor.execute(f"SELECT * FROM users WHERE nombre = '{request.form['filter']}';")
		user = cursor.fetchone()
		if not user:
			return render_template('/admin/reset_password.html', error = 'No se ha encontrado al usuario')

		if user['nombre'] in ['Josepe_Guebo', 'Patrick_Grey', 'Frank_Grey', 'Cactus_Jack', 'Konni_Moonlight']:
			return render_template('/admin/reset_password.html', error = 'Que haces boludito???')

		new_password = f'reset{random.randint(100, 200)}'
		hashed_password = hashlib.sha256(new_password.encode() + user['salt'].encode()).hexdigest().upper()

		cursor.execute(f"UPDATE users SET password = '{hashed_password}' WHERE nombre = '{request.form['filter']}';")
		mysql.connection.commit()

		return render_template('/admin/reset_password.html', success = f'La contraseña de <b>{user["nombre"]}</b> ha sido cambiada a: <b>{new_password}</b>')

	return ''

# Unban user
@admin.route("/admin/unban/user", methods = ['GET', 'POST'])
def unban_user():
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	if session['admin'] < 6:
		return redirect( url_for('admin.index') ), 302

	if request.method == 'GET':
		return render_template('/admin/unban_user.html')

	if request.method == 'POST':
		add_admin_registration(session['id'], 'Desbanear', request.form['filter'])

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

		cursor.execute(f"SELECT baneado FROM users WHERE nombre = '{request.form['filter']}' OR ultima_ip = '{request.form['filter']}';")
		user = cursor.fetchone()
		if not user:
			return render_template('/admin/unban_user.html', error = 'No se ha encontrado al usuario')

		if not user['baneado']:
			return render_template('/admin/unban_user.html', error = 'El usuario no esta baneado')

		cursor.execute(f"UPDATE users SET baneado = 0, baneo_temporal = 0, tiempo_baneo = 0 WHERE nombre = '{request.form['filter']}' OR ultima_ip = '{request.form['filter']}';")
		mysql.connection.commit()
		return render_template('/admin/unban_user.html', success = 'Usuario desbaneado')

	return ''

# Search user
@admin.route("/admin/search/user", methods = ['GET', 'POST'])
def search_user():
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	if session['admin'] < 4:
		return redirect( url_for('admin.index') ), 302

	if request.method == 'GET':
		return render_template('/admin/search_user.html')

	if request.method == 'POST':
		add_admin_registration(session['id'], 'Buscar usuario', request.form['filter'])

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(f"SELECT * FROM users WHERE email LIKE '%{escape_text(request.form['filter'])}%' OR nombre LIKE '{escape_text(request.form['filter'])}' OR ultima_ip LIKE '{escape_text(request.form['filter'])}' OR id_users LIKE '{escape_text(request.form['filter'])}' LIMIT 50;")
		users = cursor.fetchall()
		if not users:
			return render_template('/admin/search_user.html', error = 'No se encontraron usuarios.')

		for user in users:
			if user['id_users'] == 81045:
				user['ultima_ip'] = 'mama el guebo!'

		return render_template('/admin/search_user.html', users = users)

	return ''

# Search gang
@admin.route("/admin/search/gang", methods = ['GET', 'POST'])
def search_gang():
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	if session['admin'] < 3:
		return redirect( url_for('admin.index') ), 302

	if request.method == 'GET':
		return render_template('/admin/search_gang.html')

	if request.method == 'POST':
		add_admin_registration(session['id'], 'Buscar banda', request.form['filter'])

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(f"SELECT * FROM bandas WHERE nombre LIKE '%{escape_text(request.form['filter'])}%' OR dueno LIKE '{escape_text(request.form['filter'])}' OR id_usuario LIKE '{escape_text(request.form['filter'])}' LIMIT 50;")
		gangs = cursor.fetchall()
		if not gangs:
			return render_template('/admin/search_gang.html', error = 'No se encontraron bandas.')

		return render_template('/admin/search_gang.html', gangs = gangs)

	return ''

# Name historial
@admin.route("/admin/historial/usernames", methods = ['GET', 'POST'])
def usernames_historial():
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	if session['admin'] < 3:
		return redirect( url_for('admin.index') ), 302

	if request.method == 'GET':
		return render_template('/admin/name_historial.html')

	if request.method == 'POST':
		add_admin_registration(session['id'], 'Historial de nombres', request.form['filter'])

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(f"SELECT * FROM logs_cambio_nombres WHERE usuario_id LIKE '%{escape_text(request.form['filter'])}%' OR nombre_antiguo LIKE '{escape_text(request.form['filter'])}' OR nombre_nuevo LIKE '{escape_text(request.form['filter'])}' OR ip LIKE '{escape_text(request.form['filter'])}' LIMIT 50;")
		users = cursor.fetchall()
		if not users:
			return render_template('/admin/name_historial.html', error = 'No se encontraron usuarios.')

		return render_template('/admin/name_historial.html', users = users)

	return ''

# Receipts
@admin.route("/admin/receipts", methods = ['GET', 'POST'])
@admin.route("/admin/receipts/<updated>", methods = ['GET', 'POST'])
def receipts_list(updated = False):
	if not session.get('id'):
		session['last_url'] = request.url_rule.endpoint
		return redirect( url_for('auth.sign_in') ), 302

	if not session['admin'] or not session['id'] in payment_validers:
		return redirect( url_for('admin.index') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT * FROM `payments`, `shop_products` WHERE `payments`.`state` < '2' AND `shop_products`.`id` = `payments`.`product_id`;")
	payments = cursor.fetchall()
	for payment in payments:
		if payment['state'] == 0 and not payment['method'] in ['Rapipago', 'Pago fácil']:
			continue
		
		payment['valid'] = True
		payment['start_date'] = payment['start_date'].strftime("%m/%d/%Y %H:%M:%S")

	return render_template('/admin/receipts.html', payments = payments, updated = updated)

# Receipts all
@admin.route("/admin/receipts/all", methods = ['GET', 'POST'])
def receipts_all():
	if not session.get('id'):
		session['last_url'] = request.url_rule.endpoint
		return redirect( url_for('auth.sign_in') ), 302

	if not session['admin'] or not session['id'] in payment_validers:
		return redirect( url_for('admin.index') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT * FROM `payments`, `shop_products`, `users`  WHERE `payments`.`state` = '2' AND `shop_products`.`id` = `payments`.`product_id` AND `payments`.`user_id` = `users`.`id_users`;")
	payments = cursor.fetchall()

	profits = {}
	total_sales = {}
	for payment in payments:
		payment['start_date'] = payment['start_date'].strftime("%m/%d/%Y %H:%M:%S")
		payment['end_date'] = payment['end_date'].strftime("%m/%d/%Y %H:%M:%S")
		
		# Profits
		try:
			if payment['currency'] == 'UYU':
				continue

			profits[ payment['currency'] ] += payment['price']
		
		except:
			profits[ payment['currency'] ] = payment['price']

		# Sales
		try:
			if payment['currency'] == 'UYU':
				continue

			total_sales[ payment['currency'] ] += 1
		
		except:
			total_sales[ payment['currency'] ] = 1

	return render_template('/admin/receipts_all.html', payments = payments, profits = profits.items(), total_sales = total_sales)

@admin.route("/admin/dispatch_payment/<payment_id>", methods = ['GET', 'POST'])
def dispatch_payment(payment_id):
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	if not session['admin'] or not session['id'] in payment_validers:
		return redirect( url_for('admin.index') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `payments`, `shop_products`, `users` WHERE `payments`.`id` = '{escape_text(payment_id)}' AND `shop_products`.`id` = `payments`.`product_id` AND `users`.`id_users` = `payments`.`user_id`;")
	payment = cursor.fetchone()
	if not payment:
		return render_template('/info/error.html', code = 404, info = "Este pago no existe")

	if request.method == 'GET':
		count = 0
		method_id = 0
		for method in payment_methods:
			if method[0] == payment['method']:
				method_id = count
			count += 1

		return render_template('/admin/dispatch_payment.html', session = session, payment = payment, method_info = payment_methods[method_id])

	if request.method == 'POST':
		# Send code
		if request.form['state'] == '0':
			cursor.execute(f"UPDATE `payments` SET `state` = '0', `admin_id` = '{session['id']}', `response` = '{escape_text(request.form['payment_code'])}' WHERE `id` = '{escape_text(payment_id)}';")
			mysql.connection.commit()

		# Dispatch product
		if request.form['state'] == '2':
			cursor.execute(f"UPDATE `payments` SET `state` = '2', `admin_id` = '{session['id']}', `end_date` = NOW() WHERE `id` = '{escape_text(payment_id)}';")
			mysql.connection.commit()

			dispatch_product(payment['user_id'], payment['shop_products.id'])

		# Duplicatedd and denied
		if request.form['state'] in ['3', '4']:
			cursor.execute(f"UPDATE `payments` SET `state` = '{escape_text(request.form['state'])}', `admin_id` = '{session['id']}', `end_date` = NOW() WHERE `id` = '{escape_text(payment_id)}';")
			mysql.connection.commit()

		return redirect( url_for('admin.receipts_list', updated = True) ), 302

	return redirect( url_for('admin.receipts_list') ), 302

# Coin manager
@admin.route("/admin/coins", methods = ['GET', 'POST'])
def coins_list():
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	if not session['admin'] or not session['id'] in payment_validers:
		return redirect( url_for('admin.index') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	top_number = 1

	# Server coin
	cursor.execute("SELECT * from server_coin;")
	server_coin = cursor.fetchone()

	# Total coins
	cursor.execute("SELECT SUM(monedas) AS 'total_coins' FROM usuario_principal;")
	total_coins = cursor.fetchall()[0]['total_coins']

	# General stats
	server_coin['burned_coins'] = server_coin['reserves'] - total_coins
	server_coin['burned_coins'] = "{:,.0f}".format( float( server_coin['burned_coins'] ))
	server_coin['reserves'] = "{:,.0f}".format( float( server_coin['reserves'] ))
	server_coin['emission_limit'] = "{:,.0f}".format( float( server_coin['emission_limit'] ))

	# Poors
	cursor.execute("SELECT monedas FROM usuario_principal WHERE monedas < 16 AND monedas > 0;")
	poors = cursor.fetchall()
	server_coin['poor'] = "{:,.0f}".format( float(len(poors)))

	# Richs
	cursor.execute("SELECT monedas FROM usuario_principal WHERE monedas > 1000;")
	richs = cursor.fetchall()
	server_coin['richs'] = "{:,.0f}".format( float(len(richs)))

	# Average
	mean_count = []
	cursor.execute("SELECT monedas FROM usuario_principal WHERE monedas > 0 AND monedas < 1000;")
	for coin in cursor.fetchall():
		mean_count.append(coin['monedas'])

	server_coin['mean'] = "{:,.0f}".format( sum(mean_count) / len(mean_count) )

	# Players with coins
	cursor.execute("SELECT COUNT(*) AS total_users FROM usuario_principal WHERE monedas > 0;")
	players_count = cursor.fetchone()
	server_coin['total_users_with_coin'] = players_count['total_users']

	# Total player
	cursor.execute("SELECT users.ultima_conexion FROM users, usuario_principal WHERE usuario_principal.usuario_id = users.id_users AND usuario_principal.nivel > 5;")
	total_users = 0
	active_players = cursor.fetchall()

	for player in active_players:
		delta = datetime.today() - datetime.fromtimestamp(player['ultima_conexion'])
		if delta.days >= 90:
			total_users += 1

	server_coin['total_users'] = total_users
	server_coin['coin_users_pct'] = "{:,.2f}".format( server_coin['total_users_with_coin'] / server_coin['total_users'] * 100 )

	# Format
	server_coin['total_users_with_coin'] = "{:,.0f}".format( server_coin['total_users_with_coin'] )
	server_coin['total_users'] = "{:,.0f}".format( server_coin['total_users'] )
	total_coins = "{:,.0f}".format( float( total_coins ))

	cursor.execute("SELECT *, `nombre` FROM `usuario_principal`, `users` WHERE `usuario_principal`.`usuario_id` = `users`.`id_users` ORDER BY `usuario_principal`.`monedas` DESC LIMIT 100;")
	players = cursor.fetchall()
	for player in players:
		delta = datetime.today() - datetime.fromtimestamp(player['ultima_conexion'])
		player['ultima_conexion'] = datetime.fromtimestamp(player['ultima_conexion']).strftime("%m/%d/%Y %H:%M:%S")
		player['days_passed'] = delta.days
		player['months_passed'] = round(delta.days / 30, 1)
		player['top_number'] = top_number
		top_number += 1

	return render_template('/admin/coins_list.html', players = players, total_coins = total_coins, server_coin = server_coin)

# Give coins
@admin.route("/admin/coins/give", methods = ['GET', 'POST'])
def give_coins():
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	if not session['admin'] or not session['id'] in payment_validers:
		return redirect( url_for('admin.index') ), 302

	if request.method == 'GET':
		return render_template('/admin/give_coins.html')

	if request.method == 'POST':
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

		cursor.execute("SELECT * from server_coin;")
		server_coin = cursor.fetchone()

		try:
			coins = int(request.form['coins'])
		
		except:
			return render_template('/admin/give_coins.html', error = 'Ingrese un valor numérico')

		if coins < 1:
			return render_template('/admin/give_coins.html', error = 'Ingrese un valor positivo')

		if coins > server_coin['reserves']:
			return render_template('/admin/give_coins.html', error = 'No hay reservas suficientes')

		cursor.execute(f"SELECT id_users, nombre FROM users WHERE nombre = '{escape_text(request.form['username'])}';")
		user = cursor.fetchone()
		if not user:
			return render_template('/admin/give_coins.html', error = 'No se ha encontrado al usuario')

		cursor.execute(f"UPDATE server_coin SET reserves = reserves - {coins};")
		mysql.connection.commit()

		cursor.execute(f"UPDATE usuario_principal SET monedas = monedas + {coins} WHERE usuario_id = {user['id_users']};")
		mysql.connection.commit()

		add_admin_registration(session['id'], f'Dar monedas ({coins} GS)', request.form['username'])

		return render_template('/admin/give_coins.html', success = f'Se han acreditado <b>{coins} monedas</b> a <b>{user["nombre"]}</b>')

# Gift codes
@admin.route('/admin/gift_codes', methods = ['GET', 'POST'])
def gift_codes():
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	if not session['admin'] or not session['id'] in payment_validers:
		return redirect( url_for('admin.index') ), 302

	if request.method == 'GET':
		return render_template('/admin/gift_codes.html')

	return ''

# Remove GS
@admin.route("/remove_gs/pct", methods = ['GET', 'POST'])
def remove_gs_pct():
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	if not session['admin'] or not session['id'] in payment_validers:
		return redirect( url_for('admin.index') ), 302

	player_count = 0
	gs_count = 0

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT usuario_id, monedas FROM `usuario_principal` where monedas > 0;")
	players = cursor.fetchall()
	for player in players:
		pct = 15
		if player['monedas'] > 2000:
			pct = 1

		player_gs = round(player['monedas'] * pct / 100)
		gs_count += player_gs
		player_count += 1

		cursor.execute(f"UPDATE usuario_principal SET monedas = monedas + {player_gs} WHERE usuario_id = {player['usuario_id']};")
		mysql.connection.commit()

	cursor.execute(f"UPDATE server_coin SET reserves = reserves - '{gs_count}';")
	mysql.connection.commit()

	return f'players: {player_count}, gs: {gs_count}'