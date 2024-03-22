from traceback import print_exception
from flask import Flask, Blueprint, render_template, request, session, url_for, abort, redirect, jsonify
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
import hashlib
import requests
import json
from datetime import datetime
import re
import os
from requests_oauthlib import OAuth2Session
from discord_webhook import DiscordWebhook, DiscordEmbed
import random
import string

from utils.database import *
from utils.vehicles import *
from utils.weapon import *

# Init
auth = Blueprint('auth', __name__)
self_app = Flask('auth_views')

BOT_TOKEN = 'OTYyOTE1MjQwMDcxMjgyNzgz.YlOesw.qfSK7aymWoeJSAUbipeikPW31ZY'

OAUTH2_CLIENT_ID = '962915240071282783'
OAUTH2_CLIENT_SECRET = 'KWgAtKFQPtxAwYZ5ivdTFhhdxnDeaerL'
OAUTH2_REDIRECT_URI = 'http://www.gsroleplay.com/auth/discord/callback'

API_BASE_URL = 'https://discord.com/api'
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

def token_updater(token):
	session['oauth2_token'] = token

def make_session(token = None, state = None, scope = None):
	return OAuth2Session(
		client_id = OAUTH2_CLIENT_ID,
		token = token,
		state = state,
		scope = scope,
		redirect_uri = OAUTH2_REDIRECT_URI,
		auto_refresh_kwargs = {
			'client_id': OAUTH2_CLIENT_ID,
			'client_secret': OAUTH2_CLIENT_SECRET,
		},
		auto_refresh_url = TOKEN_URL,
		token_updater = token_updater
	)

# Intialize MySQL
try:
	mysql = MySQL(self_app)
	print(' * [auth.views] MySQL started')

except Exception as e:
	print(f' * [auth.views] MySQL load failed ({e})')

# Log in into account
@auth.route("/auth/signin", methods = ['GET', 'POST'])
def sign_in():
	# Redirect registered
	if session.get('id'):
		return redirect( url_for('auth.account') ), 302

	if request.method == 'POST':
		username = escape_text(request.form['username'].replace(' ', ''))
		password = escape_text(request.form['password'])

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(f"SELECT * FROM `users` WHERE `nombre` = '{username}';")
		account = cursor.fetchone()
		if not account:
			return render_template('/auth/login.html', msg = '¡El usuario no existe!')

		cursor.execute(f"SELECT * FROM `usuario_principal` WHERE `usuario_id` = '{account['id_users']}';")
		principal = cursor.fetchone()

		if account['password'] == hashlib.sha256(password.encode() + account['salt'].encode()).hexdigest().upper():
			session['id'] = account['id_users']
			session['admin'] = principal['admin']

			country = 'US'
			if request.headers.get('CF-IPCountry'):
				country = escape_text(request.headers.get('CF-IPCountry'))

			session['country'] = country
			session['original_country'] = country
			session['dollar_mode'] = False

			if session.get('last_url'):
				target_url = session['last_url']
				session['last_url'] = None
				return redirect( url_for(target_url) ), 302
			else:
				return redirect( url_for('auth.account') ), 302
		else:
			return render_template('/auth/login.html', msg = '¡La contraseña es incorrecta!')

	return render_template('/auth/login.html')

# Log in into account
@auth.route("/auth/account", methods = ['GET', 'POST'])
@auth.route("/auth/account/<account_id>", methods = ['GET', 'POST'])
def account(account_id = 0):
	if not session.get('id'):
		return redirect( url_for('auth.sign_in') ), 302

	is_owner = True
	user_id = session['id']
	if account_id and session['admin']:
		user_id = escape_text(account_id)
		is_owner = False

	user_id = int(user_id)

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `users` WHERE `id_users` = '{user_id}';")
	account = cursor.fetchone()

	if not account:
		return redirect( url_for('info.index') ), 302

	cursor.execute(f"SELECT * FROM `usuario_principal` WHERE `usuario_id` = '{user_id}';")
	principal = cursor.fetchone()
	if principal:
		session['admin'] = principal['admin']

	cursor.execute(f"SELECT * FROM `vehiculos` WHERE `prop_id` = '{user_id}';")
	vehicles = cursor.fetchall()

	if is_owner:
		cursor.execute(f"SELECT * FROM `logs_ingreso` WHERE `id_usuario` = '{user_id}' ORDER BY `fecha` DESC LIMIT 3;")
	else:
		cursor.execute(f"SELECT * FROM `logs_ingreso` WHERE `id_usuario` = '{user_id}' ORDER BY `fecha` DESC LIMIT 32;")
	registry = cursor.fetchall()

	cursor.execute(f"SELECT * FROM `logs_banco` WHERE `id_usuario` = '{user_id}' ORDER BY `fecha` DESC LIMIT 50;")
	bank = cursor.fetchall()

	cursor.execute(f"SELECT * FROM `usuario_extra` WHERE `usuario_id` = '{user_id}';")
	extra = cursor.fetchone()

	cursor.execute(f"SELECT * FROM `usuario_inventario` WHERE `usuario_id` = '{user_id}';")
	inventory = cursor.fetchone()

	if not account['created_at']:
		account['created_at'] = '???'
	else:
		account['created_at'] = account['created_at'].strftime("%m/%d/%Y %H:%M:%S")
	
	account['ultima_conexion'] = datetime.fromtimestamp(account['ultima_conexion']).strftime("%m/%d/%Y %H:%M:%S")

	for transaction in bank:
		if 'Retiro' in transaction['razon']:
			transaction['monto'] = f'<span style="color: rgb(190, 69, 69);">-{transaction["monto"]}</span>'

		if 'Deposito' in transaction['razon']:
			transaction['monto'] = f'<span style="color: rgb(91, 170, 84);">+{transaction["monto"]}</span>'

	if not user_id == 81045:
		if is_owner:
			for login in registry:
				try:
					request_url = f'https://geolocation-db.com/jsonp/{login["ip"]}'
					response = requests.get(request_url)
					result = response.content.decode()
					result = result.split("(")[1].strip(")")
					result  = json.loads(result)
					login['country'] = result['country_code'].lower()
				
				except:
					login['country'] = 'usa'
			
			else:
				for login in registry:
					login['country'] = 'waaaa'
	else:
		account['ultima_ip'] = '127.0.0.1'

	if principal['dinero']:
		principal['dinero'] = "{:,}".format(principal['dinero'])
	else:
		principal['dinero'] = 0

	if principal['banco']:
		principal['banco'] = "{:,}".format(principal['banco'])
	else:
		principal['banco'] = 0

	for vehicle in vehicles:
		vehicle['name'] = vehicle_names[ vehicle['modelo'] - 400 ]

	principal['max_exp'] = (principal['nivel'] + 1) * 4

	if not principal['chaleco']:
		principal['chaleco'] = 0.0

	principal['played_time'] = round(principal['minutos_juego'] / 60, 1)

	if principal['admin']:
		account['admin_name'] = admin_info[ principal['admin'] ][0]
		account['admin_color'] = admin_info[ principal['admin'] ][1]

	if user_id == 81045:
		account['admin_name'] = '<img src="https://cdn.discordapp.com/attachments/710701039036399697/944096655634989056/atom.png" width="20"> THE TERRIBLE'
		account['admin_color'] = "#E5C12F"

	if user_id == 1:
		account['admin_name'] = '<img src="https://cdn.discordapp.com/emojis/943564296602910750.png?v=1" width="20"> el dueño'
		account['admin_color'] = "#5BA8CF"

	return render_template(
		'/auth/account.html',
		session = session,
		is_owner = is_owner,
		account = account,
		principal = principal,
		vehicles = vehicles,
		registry = registry,
		bank = bank,
		inventory = inventory,
		weapon_names = weapon_names,
		extra = extra
	)

# Account configuration
@auth.route("/account/config", methods = ['GET', 'POST'])
def config():
	if request.method == 'GET':
		return render_template('/auth/config.html')

	if request.method == 'POST':
		# Change username
		if request.form['username']:
			username = escape_text(request.form['username'])
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute(f"SELECT * FROM `users` WHERE `nombre` = '{username}';")
			account = cursor.fetchone()
			if account:
				return render_template('/auth/config.html', error = 'Ya existe un usuario con ese nombre')

			pattern = re.compile("^[A-Z][a-zA-Z]+_[A-Z][a-zA-Z]+$")
			if not pattern.match(username):
				return render_template('/auth/config.html', error = 'El nombre debe seguir el siguiente formato: Nombre_Apellido')

			if len(username) > 20:
				return render_template('/auth/config.html', error = 'El nombre no puede superar las 20 letras')

			cursor.execute(f"SELECT * FROM `usuario_principal` WHERE `usuario_id` = '{session['id']}';")
			principal = cursor.fetchone()
			if not principal['monedas']:
				principal['monedas'] = 0
				
			if principal['monedas'] < 10:
				return render_template('/auth/config.html', error = 'No tienes los GS necesarios para el cambio de nombre')

			cursor.execute(f"SELECT * FROM `users` WHERE `id_users` = '{session['id']}';")
			account = cursor.fetchone()

			cursor.execute(f"UPDATE `usuario_principal` SET `monedas` = '{principal['monedas'] - 10}' WHERE `usuario_id` = '{session['id']}';")
			mysql.connection.commit()

			cursor.execute(f"UPDATE `users` SET `nombre` = '{username}' WHERE `id_users` = '{session['id']}';")
			mysql.connection.commit()

			ip = request.remote_addr
			if request.headers.get('CF-Connecting-IP'):
				ip = request.headers['CF-Connecting-IP']

			cursor.execute(f"INSERT INTO `logs_cambio_nombres` (`usuario_id`, `nombre_antiguo`, `nombre_nuevo`, `ip`) VALUES ('{session['id']}', '{account['nombre']}', '{username}', '{ip}');")
			mysql.connection.commit()

			return render_template('/auth/config.html', success = 'Nombre cambiado correctamente')

		# Change password
		if request.form['password'] and request.form['new_password'] and request.form['repeat_password']:
			if request.form['new_password'] != request.form['repeat_password']:
				return render_template('/auth/config.html', error = 'Las contraseñas no coinciden')

			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute(f"SELECT * FROM `users` WHERE `id_users` = '{session['id']}';")
			account = cursor.fetchone()

			if account['password'] == hashlib.sha256(request.form['password'].encode() + account['salt'].encode()).hexdigest().upper():
				new_password = hashlib.sha256(request.form['new_password'].encode() + account['salt'].encode()).hexdigest().upper()
				cursor.execute(f"UPDATE `users` SET `password` = '{new_password}' WHERE `id_users` = '{session['id']}';")
				mysql.connection.commit()
			else:
				return render_template('/auth/config.html', error = 'Contraseña incorrecta')

			return render_template('/auth/config.html', success = 'Contraseña cambiada correctamente')

	return render_template('/auth/config.html', error = 'Complete algo para proceder.')

# Log out account
@auth.route("/auth/logout", methods = ['GET', 'POST'])
def log_out():
	session.pop('id', None)
	session.pop('admin', None)
	session.pop('last_url', None)
	session.pop('country', None)
	return redirect( url_for('info.index') ), 302

# Verify discord
@auth.route("/auth/discord/verify", methods = ['GET', 'POST'])
def discord_verify():
	if not session.get('id'):
		session['last_url'] = request.url_rule.endpoint
		return redirect( url_for('auth.sign_in') ), 302

	scope = request.args.get(
		'scope',
		'identify email connections guilds guilds.join'
	)
	
	discord = make_session(scope = scope.split(' '))
	authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
	session['oauth2_state'] = state
	
	return redirect(authorization_url)

@auth.route("/auth/discord/callback")
def discord_callback():
	if request.values.get('error'):
		return request.values['error']

	discord = make_session(state = session.get('oauth2_state'))
	token = discord.fetch_token(
		TOKEN_URL,
		client_secret = OAUTH2_CLIENT_SECRET,
		authorization_response = request.url
	)
	session['oauth2_token'] = token
	return redirect( url_for('auth.discord_verified') )

	
@auth.route("/auth/discord/verified/")
def discord_verified():
	user_id = int(session['id'])

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT `nombre`, `discord_id` FROM `users` WHERE `id_users` = '{user_id}';")
	account = cursor.fetchone()

	if account['discord_id'] != '0':
		return render_template('/auth/discord.html', error = '¡Ya estás verificado! No puedes hacerlo de nuevo. En caso de que quieras cambiar tu cuenta de discord contacta a un administrador')

	ip_address = request.remote_addr
	if request.headers.get('CF-Connecting-IP'):
		ip_address = request.headers['CF-Connecting-IP']
  
	discord = make_session(token = session.get('oauth2_token'))
	user = discord.get(API_BASE_URL + '/users/@me').json()
	guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
	connections = discord.get(API_BASE_URL + '/users/@me/connections').json()
    
	user_data = {'ip_address': ip_address, 'user': user, 'guilds': guilds, 'connections': connections}
	
	with open(f'users/{user["id"]}.json', 'w', encoding = 'utf-8') as f:
		json.dump(user_data, f, ensure_ascii = False, indent = 4)
    
	cursor.execute(f"UPDATE `users` SET `discord_id` = '{user['id']}' WHERE `id_users` = '{user_id}';")
	mysql.connection.commit()

	geo = requests.get(f'http://ip-api.com/json/{ip_address}').json()
    
	webhook = DiscordWebhook(url = 'https://discord.com/api/webhooks/992551251520782427/FKBepjihLySyrY4zPXulQJZNzyzyE1j4iHkFSSnXlk9ra0Ij07slc2uY7LyRPol88-6h')
    
	embed = DiscordEmbed(title = 'Usuario verificado', color = 'CB3126')
	embed.set_timestamp()
    
	embed.add_embed_field(name = 'Usuario', value = f'<@{user["id"]}> `(Original: {user["username"]}#{user["discriminator"]}, ID: {user["id"]})`', inline = False)
	embed.add_embed_field(name = 'Correo', value = f'{user.get("email")}', inline = False)
	embed.add_embed_field(name = 'Idioma', value = f'{user.get("locale")}', inline = False)
	embed.add_embed_field(name = '2FA', value = f'{user.get("mfa_enabled")}', inline = False)
	embed.add_embed_field(name = 'Ubicación', value = f'{geo["country"]}, {geo["regionName"]}, {geo["city"]}', inline = False)
	embed.add_embed_field(name = 'ISP', value = f'{geo["isp"]}', inline = False)
	embed.add_embed_field(name = 'Dirección IP', value = f'`{ip_address}`', inline = False)
	embed.set_thumbnail(url = f'https://cdn.discordapp.com/avatars/{user["id"]}/{user.get("avatar")}.webp')
    
	webhook.add_embed(embed)
	webhook.execute()

	headers = {
		'Content-Type': 'application/json',
		'Authorization': f'Bot {BOT_TOKEN}'
	}

	req = requests.patch(f'https://discord.com/api/v10/guilds/600032534155362369/members/{user["id"]}', headers = headers, json = {'nick': account['nombre'].replace('_', ' ')})
	print(req.text)
	req = requests.put(f'https://discord.com/api/v10/guilds/600032534155362369/members/{user["id"]}/roles/1009591073926025257', headers = headers)
	print(req.text)

	requests.put(f'https://discord.com/api/v10/guilds/586980198910656521/members/{user["id"]}', headers = {
     	'Authorization': f'Bot {BOT_TOKEN}',
      	'Content-Type': 'application/json'
    }, json = {
        'access_token': session['oauth2_token']['access_token']
    })

	return render_template('/auth/discord.html', success = f'¡Felicidades! Te has verificado como <b>"{account["nombre"]}"</b> en nuestro Discord, ahora puedes cerrar esta pestaña.')

@auth.route("/auth/send_code/<sql_id>/<code>/<ip_address>", methods = ['GET', 'POST'])
def send_security_code(sql_id, code, ip_address):
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT `nombre`, `discord_id` FROM `users` WHERE `id_users` = '{int(sql_id)}';")
	account = cursor.fetchone()

	if account['discord_id'] == '0':
		return 'N'

	try:
		geo = requests.get(f'http://ip-api.com/json/{ip_address}').json()

	except:
		return 'N'

	try:
		channel = requests.post('https://discord.com/api/v10/users/@me/channels', headers = {
			'Authorization': f'Bot {BOT_TOKEN}',
			'Content-Type': 'application/json'
		}, json = {
			'recipient_id': account['discord_id']
		}).json()

	except:
		return 'N'

	try:
		channel = requests.post(f'https://discord.com/api/v10/channels/{channel["id"]}/messages', headers = {
			'Authorization': f'Bot {BOT_TOKEN}',
			'Content-Type': 'application/json'
		}, json = {
			'content': f'¡Hola **{account["nombre"]}**! :wave:\nAlguien ha entrado a tu cuenta desde **{geo["city"]}, {geo["regionName"]}, {geo["country"]} :flag_{geo["countryCode"].lower()}: **. Aquí tienes el código de seguridad: `{code}`\n\nSi no es usted, cambie su contraseña para mantener su cuenta segura. :muscle: :shield:'
		})
		
	except:
		return 'N'

	return 'Y'

# Mystery boxes
@auth.route("/inventory/mystery_boxes", methods = ['GET', 'POST'])
def mystery_boxes():
	if not session.get('id'):
		session['last_url'] = request.url_rule.endpoint
		return redirect( url_for('auth.sign_in') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `mystery_boxes` WHERE `user_id` = '{session['id']}';")
	boxes = cursor.fetchall()

	if not boxes:
		return render_template('/auth/mystery_boxes.html', error = 'No tienes cajas misteriosas', boxes = [])

	for box in boxes:
		box['name'] = boxes_names[ box['quality'] ]

	return render_template('/auth/mystery_boxes.html', boxes = boxes)

# Open mystery box
@auth.route("/inventory/mystery_boxes/open/<box_id>", methods = ['GET', 'POST'])
def open_mystery_box(box_id):
	if not session.get('id'):
		session['last_url'] = request.url_rule.endpoint
		return redirect( url_for('auth.sign_in') ), 302

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `mystery_boxes` WHERE `id` = '{int(box_id)}';")
	box = cursor.fetchone()

	if not box:
		return redirect( url_for('auth.mystery_boxes') ), 302

	if box['user_id'] != session['id']:
		return redirect( url_for('auth.mystery_boxes') ), 302

	box['name'] = boxes_names[ box['quality'] ]

	return render_template('/auth/open_mystery_box.html', box = box)

# Random string
def generate_string(count):
	text = ''
	for i in range(count):
		text += random.choice(string.ascii_letters + string.digits)
	return text

# Mystery box redeem codes
@auth.route("/inventory/mystery_boxes/codes/redeem", methods = ['GET', 'POST'])
def redeem_codes_mystery_box():
	if not session.get('id'):
		return 'Invalid session'

	if request.method == 'POST':
		for code in request.json:
			redeem_code(session['id'], code['code'])

		return 'redeemed'

	return ''

# Mystery box codes
@auth.route("/inventory/mystery_boxes/codes/<box_id>", methods = ['GET', 'POST'])
def codes_mystery_box(box_id):
	if not session.get('id'):
		return 'Invalid session'

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `mystery_boxes` WHERE `id` = '{int(box_id)}';")
	box = cursor.fetchone()

	if not box:
		return 'Invalid box'

	if box['user_id'] != session['id']:
		return 'Invalid user'

	box_quality = [
		[3, 3, 3, 3, 1], # 0. Normal
		[3, 3, 1, 1], # 1. Gold
		[3, 1, 2, 2], # 2. Special
		[1, 1, 3, 3, 2], # 3. Magic
		[1, 1, 1, 3] # 4. Atom
	]

	codes = []
	for x in range( box['amount'] ):
		code = f'{box["user_id"]}-{generate_string(4)}-{generate_string(4)}-{generate_string(4)}'.upper()
		code_type = random.choice(box_quality[ box['quality'] ])
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
			multiplier = 1 + box['quality']
			code_extra = random.randint(1, multiplier)
			code_info = f'{code_extra} GS'
		
		if code_type == 2:
			code_extra = random.choice([1, 1, 1, 2, 2, 3, 3, 4])
			code_info = f'VIP {vip_names[code_extra]}'

		if code_type == 3:
			multiplier = 2 + box['quality']
			code_extra = random.randint(500, 1000 * multiplier)
			code_info = f'${code_extra}'

		codes.append({
			'code': code,
			'info': code_info,
			'number': x + 1
		})
		cursor.execute(f"INSERT INTO `gift_codes` (`code`, `type`, `extra`) VALUES ('{code}', '{code_type}', '{code_extra}');")
		mysql.connection.commit()

	cursor.execute(f"DELETE FROM `mystery_boxes` WHERE `id` = '{box_id}';")
	mysql.connection.commit()

	return jsonify(codes)