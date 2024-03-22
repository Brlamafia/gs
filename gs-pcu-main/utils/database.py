from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
import time

# MySQL
self_app = Flask('info_views')

# Intialize MySQL
try:
	mysql = MySQL(self_app)
	print(' * [utils] MySQL started')

except Exception as e:
	print(f' * [utils] MySQL load failed ({e})')

boxes_names = [
	'Caja normal',
	'Caja dorada',
	'Caja especial',
	'✨ Caja mágica ✨',
	'Caja Atom'
]

admin_info = [
	["Usuario", "#FFFFFF"], # 0
	["Ayudante", "#4AA8DD"], # 1
	["Soporte", "#6BBA60"], # 2
	["Moderador (1)", "#6BBA60"], # 3
	["Moderador (2)", "#6BBA60"], # 4
	["Moderador (3)", "#6BBA60"], # 5
	["Moderador (4)", "#D65858"], # 6
	["Moderador Global", "#CFC54F"], # 7
	["Co-Admin", "#CFC54F"], # 8
	["Administrador", "#D65858"], # 9
	["OP", "#E58D2F"], # 10
	["Dueño", "#F1C01C"] # 11
]

# Utils
def escape_text(text):
	return MySQLdb._mysql.escape_string(text).decode()

def dispatch_product(user_id, product_id):
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `shop_products` WHERE `id` = '{product_id}';")
	product = cursor.fetchone()
	if not product:
		return False

	# GS Coin
	if product['type'] == 0:
		cursor.execute(f"UPDATE server_coin SET reserves = reserves - {product['extra']};")
		mysql.connection.commit()

		cursor.execute(f"SELECT `monedas` FROM `usuario_principal` WHERE `usuario_id` = '{user_id}';")
		result = cursor.fetchone()
		if not result['monedas']:
			cursor.execute(f"UPDATE `usuario_principal` SET `monedas` = '{product['extra']}' WHERE `usuario_id` = '{user_id}';")
		else:
			cursor.execute(f"UPDATE `usuario_principal` SET `monedas` = `monedas` + '{product['extra']}' WHERE `usuario_id` = '{user_id}';")
		
		mysql.connection.commit()

	# VIP
	if product['type'] == 1:
		vip_duration = int(time.time()) + (31 * 86400)
		if product['extra'] == 4:
			vip_duration = int(time.time()) + (35 * 86400)

		cursor.execute(f"UPDATE `usuario_principal` SET `vip` = '{product['extra']}', `tiempo_vip` = '{vip_duration}' WHERE `usuario_id` = '{user_id}';")
		mysql.connection.commit()

	# VIP DIAMOND
	if product['type'] == 2:
		vip_duration = int(time.time()) + (62 * 86400)

		cursor.execute(f"UPDATE `usuario_principal` SET `vip` = '4', `tiempo_vip` = '{vip_duration}' WHERE `usuario_id` = '{user_id}';")
		mysql.connection.commit()

	# VEHICLE
	if product['type'] == 10:
		print(f"INSERT INTO vehiculos (posx,posy,posz,posangle,parkx,parky,parkz,parkangle,virtual_world,interior,prop_id,modelo,paintjob,color_1,color_2,matricula,spawneado,organizacion) VALUES (0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,{user_id},{product['extra']},0,0,0,'C4SH 69',0,-1);")
		cursor.execute(f"INSERT INTO vehiculos (posx,posy,posz,posangle,parkx,parky,parkz,parkangle,virtual_world,interior,prop_id,modelo,paintjob,color_1,color_2,matricula,spawneado,organizacion) VALUES (0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0,0,{user_id},{product['extra']},0,0,0,'C4SH 69',0,-1);")
		mysql.connection.commit()

	# NORMAL BOX
	if product['type'] == 50:
		for x in range( int(product['extra']) ):
			cursor.execute(f"INSERT INTO `mystery_boxes` (`quality`, `user_id`) VALUES ('0', '{user_id}');")
			mysql.connection.commit()

	# GOLD BOX
	if product['type'] == 51:
		for x in range( int(product['extra']) ):
			cursor.execute(f"INSERT INTO `mystery_boxes` (`quality`, `user_id`) VALUES ('1', '{user_id}');")
			mysql.connection.commit()

	# SPECIAL BOX
	if product['type'] == 52:
		for x in range( int(product['extra']) ):
			cursor.execute(f"INSERT INTO `mystery_boxes` (`quality`, `user_id`) VALUES ('2', '{user_id}');")
			mysql.connection.commit()

	return True

def give_vip(user_id, vip, days):
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	vip_duration = int(time.time()) + (days * 86400)

	cursor.execute(f"UPDATE `usuario_principal` SET `vip` = '{vip}', `tiempo_vip` = '{vip_duration}' WHERE `usuario_id` = '{user_id}';")
	mysql.connection.commit()
	return True

def remove_coins(user_id, count):
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `usuario_principal` WHERE `usuario_id` = '{user_id}';")
	principal = cursor.fetchone()
	if principal['monedas'] < count:
		return False

	cursor.execute(f"UPDATE `usuario_principal` SET `monedas` = '{principal['monedas'] - count}' WHERE `usuario_id` = '{user_id}';")
	mysql.connection.commit()
	return True

def add_admin_registration(admin_id, action_name, filter):
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"SELECT * FROM `users` WHERE `id_users` = '{admin_id}';")
	user = cursor.fetchone()
	if user:
		admin_name = user['nombre']
	else:
		admin_name = f'ID {admin_id}'

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(f"INSERT INTO `admin_registry` (`admin_name`, `action_name`, `filter`) VALUES ('{escape_text(admin_name)}', '{escape_text(action_name)}', '{escape_text(filter)}');")
	mysql.connection.commit()

def redeem_code(user_id, code):
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

	cursor.execute(f"SELECT * FROM gift_codes WHERE code = '{code}';")
	code_info = cursor.fetchone()
	if not code_info:
		return 'INVALID CODE'

	if code_info['user_id']:
		cursor.execute(f"SELECT nombre FROM users WHERE id_users = '{code_info['user_id']}';")
		account = cursor.fetchone()
		if not account:
			account['nombre'] = 'Deleted User'

		return f'REDEEMED,{account["nombre"]}'

	cursor.execute(f"UPDATE gift_codes SET user_id = '{user_id}' WHERE id = '{code_info['id']}';")
	mysql.connection.commit()

	redeemed = ''

	# GS
	if code_info['type'] == 1:
		cursor.execute(f"UPDATE server_coin SET reserves = reserves - {code_info['extra']};")
		mysql.connection.commit()

		cursor.execute(f"SELECT `monedas` FROM `usuario_principal` WHERE `usuario_id` = '{user_id}';")
		result = cursor.fetchone()
		if not result['monedas']:
			cursor.execute(f"UPDATE `usuario_principal` SET `monedas` = '{code_info['extra']}' WHERE `usuario_id` = '{user_id}';")
			
		else:
			cursor.execute(f"UPDATE `usuario_principal` SET `monedas` = `monedas` + '{code_info['extra']}' WHERE `usuario_id` = '{user_id}';")
			
		mysql.connection.commit()
		redeemed = f"Has canjeado {code_info['extra']} GS"

	# VIP
	if code_info['type'] == 2:
		vip_duration = int(time.time()) + (31 * 86400)

		cursor.execute(f"UPDATE `usuario_principal` SET `vip` = '{code_info['extra']}', `tiempo_vip` = '{vip_duration}' WHERE `usuario_id` = '{user_id}';")
		mysql.connection.commit()

		vip_names = [
			'NINGUNO',
			'BRONZE',
			'SILVER',
			'GOLD',
			'DIAMANTE'
		]

		redeemed = f"Has canjeado VIP {vip_names[code_info['extra']]} por un mes"

	# Money
	if code_info['type'] == 3:
		cursor.execute(f"UPDATE `usuario_principal` SET `dinero` = `dinero` + '{code_info['extra']}' WHERE `usuario_id` = '{user_id}';")
		mysql.connection.commit()

		redeemed = f"Has canjeado ${code_info['extra']}"

	# Boxes
	if code_info['type'] == 100:
		cursor.execute(f"INSERT INTO `mystery_boxes` (`quality`, `user_id`) VALUES ('{code_info['extra']}', '{user_id}');")
		mysql.connection.commit()

		redeemed = f"Has canjeado una {boxes_names[code_info['extra']]}"
			
	return redeemed