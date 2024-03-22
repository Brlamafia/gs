from flask import Flask, Blueprint, render_template, request, session, url_for, abort, redirect, jsonify
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
import textwrap
import random
import operator
from utils.database import *
from utils.vehicles import *

# Init
info = Blueprint('info', __name__)

# MySQL
self_app = Flask('info_views')

# Intialize MySQL
try:
	mysql = MySQL(self_app)
	print(' * [info.views] MySQL started')

except Exception as e:
	print(f' * [info.views] MySQL load failed ({e})')

# index
@info.route("/", methods = ['GET', 'POST'])
def index():
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT *, `nombre` FROM `noticias`, `users` WHERE `noticias`.`user_id` = `users`.`id_users` ORDER BY `noticias`.`created_at` DESC;")
	news = cursor.fetchall()

	for new in news:
		new['short'] = textwrap.shorten(new['texto'], width = 128)
		new['created_at'] = new['created_at'].strftime("%m/%d/%Y a las %H:%M:%S")

	cursor.execute("SELECT `id_users` FROM `users` WHERE `conectado` = '1';")
	connected = len(cursor.fetchall()) + random.randint(0, 5)

	return render_template('/info/index.html', news = news, connected = connected)

# Discord
@info.route("/discord", methods = ['GET', 'POST'])
def discord_invite():
	return redirect('https://discord.gg/FJRyJZxxsC'), 302

# Top
@info.route("/top/<top_id>", methods = ['GET', 'POST'])
def top(top_id):
	top_id = int(top_id)
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	top_number = 1

	if top_id == 0:
		cursor.execute("SELECT *, `nombre` FROM `usuario_principal`, `users` WHERE `usuario_principal`.`usuario_id` = `users`.`id_users` ORDER BY `usuario_principal`.`dinero` DESC LIMIT 10;")
		players = cursor.fetchall()
		for player in players:
			if top_number == 1:
				player['nombre'] = '<i class="em em-money_mouth_face" aria-role="presentation" aria-label="MONEY-MOUTH FACE"></i> ' + player['nombre']

			if player['dinero']:
				player['dinero'] = "{:,}".format(player['dinero'] + player['banco'])
			else:
				player['dinero'] = 0

			player['top_number'] = top_number
			top_number += 1

		return render_template('/info/top_0.html', players = players)

	if top_id == 1:
		cursor.execute("SELECT *, `nombre` FROM `usuario_principal`, `users` WHERE `usuario_principal`.`usuario_id` = `users`.`id_users` ORDER BY `usuario_principal`.`monedas` DESC LIMIT 10;")
		players = cursor.fetchall()
		for player in players:
			if top_number == 1:
				player['nombre'] = '<i class="em em-money_with_wings" aria-role="presentation" aria-label="MONEY WITH WINGS"></i> ' + player['nombre']

			player['top_number'] = top_number
			top_number += 1

		return render_template('/info/top_1.html', players = players)

	if top_id == 2:
		cursor.execute("SELECT *, `nombre` FROM `usuario_principal`, `users` WHERE `usuario_principal`.`usuario_id` = `users`.`id_users` ORDER BY `usuario_principal`.`minutos_juego` DESC LIMIT 10;")
		players = cursor.fetchall()
		for player in players:
			if top_number == 1:
				player['nombre'] = '<i class="em em-joy" aria-role="presentation" aria-label="FACE WITH TEARS OF JOY"></i> ' + player['nombre']

			player['top_number'] = top_number
			player['minutos_juego'] = round(player['minutos_juego'] / 24 / 60, 1)
			top_number += 1

		return render_template('/info/top_2.html', players = players)

	if top_id == 3:
		cursor.execute("SELECT *, `skin`, `nombre` FROM `usuario_extra`, `usuario_principal`, `users` WHERE `usuario_extra`.`usuario_id` = `users`.`id_users` AND `usuario_principal`.`usuario_id` = `users`.`id_users` ORDER BY `usuario_extra`.`jails` DESC LIMIT 10;")
		players = cursor.fetchall()
		for player in players:
			if top_number == 1:
				player['nombre'] = '<i class="em em-clown_face" aria-role="presentation" aria-label="CLOWN FACE"></i> ' + player['nombre']

			player['top_number'] = top_number
			top_number += 1

		return render_template('/info/top_3.html', players = players)

	if top_id == 4:
		cursor.execute("SELECT *, `nombre` FROM `usuario_principal`, `users` WHERE `usuario_principal`.`usuario_id` = `users`.`id_users` AND `usuario_principal`.`admin` > '0' ORDER BY `usuario_principal`.`admin` DESC;")
		players = cursor.fetchall()

		for player in players:
			player['admin_name'] = admin_info[ player['admin'] ][0]
			player['admin_color'] = admin_info[ player['admin'] ][1]
			player['top_number'] = top_number

			if player['id_users'] == 81045:
				player['admin_name'] = '<img src="https://cdn.discordapp.com/attachments/710701039036399697/944096655634989056/atom.png" width="20"> THE TERRIBLE'
				player['admin_color'] = "#E5C12F"

			if player['id_users'] == 1:
				player['admin_name'] = '<img src="https://cdn.discordapp.com/emojis/943564296602910750.png?v=1" width="20"> el dueño'
				player['admin_color'] = "#5BA8CF"

			top_number += 1

		return render_template('/info/top_4.html', players = players)

	if top_id == 5:
		cursor.execute("SELECT `admin_nombre`, `user_nombre`, `razon`, `tipo_san`, `fecha` FROM `logs_baneos` ORDER BY `fecha` DESC LIMIT 500;")
		players = cursor.fetchall()

		type_names = [
			'Ban',
			'Jail',
			'Kick'
		]

		for player in players:
			player['tipo_san'] = type_names[player['tipo_san']]

		return render_template('/info/top_5.html', players = players)

	if top_id == 6:
		cursor.execute("SELECT user_id, COUNT(*) AS total_boxes FROM mystery_boxes GROUP BY user_id ORDER BY total_boxes DESC LIMIT 10;")
		players = cursor.fetchall()
		for player in players:
			cursor.execute(f"SELECT nombre, skin FROM users, usuario_principal WHERE users.id_users = {player['user_id']} AND usuario_principal.usuario_id = users.id_users;")
			player_info = cursor.fetchone()
			player['nombre'] = player_info['nombre']
			player['skin'] = player_info['skin']
			player['top_number'] = top_number

			if top_number == 1:
				player['nombre'] = '<i class="em em-gift" aria-role="presentation" aria-label="WRAPPED PRESENT"></i> ' + player['nombre']

			top_number += 1

		return render_template('/info/top_6.html', players = players)

	return 'mamaguebo'

# Value calculator
@info.route("/calculator", methods = ['GET', 'POST'])
def value_calculator():
	if not session.get('id'):
		session['last_url'] = request.url_rule.endpoint
		return redirect( url_for('auth.sign_in') ), 302

	if request.method == 'GET':
		return render_template('/info/value_calculator.html')

	if request.method == 'POST':
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

		cursor.execute(f"SELECT * FROM users WHERE nombre = '{escape_text(request.form['username'])}';")
		account = cursor.fetchone()
		if not account:
			return render_template('/info/value_calculator.html', error = 'No se ha encontrado al usuario')

		value = 0

		cursor.execute(f"SELECT * FROM `usuario_principal` WHERE `usuario_id` = '{account['id_users']}';")
		principal = cursor.fetchone()

		cursor.execute(f"SELECT * FROM `usuario_inventario` WHERE `usuario_id` = '{account['id_users']}';")
		invnetory = cursor.fetchone()

		cursor.execute(f"SELECT * FROM `vehiculos` WHERE `prop_id` = '{account['id_users']}';")
		vehicles = cursor.fetchall()

		cursor.execute(f"SELECT * FROM `casas` WHERE `prop_id` = '{account['id_users']}';")
		homes = cursor.fetchall()

		if principal['nivel']:
			value += principal['nivel']

		if principal['vip']:
			value += 2 * principal['vip']

		if principal['monedas']:
			value += 0.05 * principal['monedas']

		if principal['dinero']:
			value += 0.00000015 * principal['dinero']

		if invnetory['crack']:
			value += 0.0004 * invnetory['crack']

		if invnetory['medicamentos']:
			value += 0.0003 * invnetory['medicamentos']

		for vehicle in vehicles:
			vehicle_info = vehicles_price[ vehicle['modelo'] - 400 ]

			if vehicle_info[4]:
				if vehicle_info[5] > 100:
					value += 0.01 * vehicle_info[5]
			else:
				value += 0.01 * ( vehicle_info[5] / 200000)

		for home in homes:
			value += 10

		if  principal['admin']:
			value += 35 * principal['admin']

		account['skin'] = principal['skin']

		return render_template('/info/value_calculator.html', player = account, value = round(value / 2, 1))