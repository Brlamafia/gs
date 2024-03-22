# Flask
import config
import mercadopago
from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

# Application config
app = Flask(__name__, template_folder = './')
app.secret_key = 'acw3racety6u7i78o76r5rvsefsgr5434567uhgfdd'
app.config['MYSQL_HOST'] = config.mysql_host
app.config['MYSQL_USER'] = config.mysql_user
app.config['MYSQL_PASSWORD'] = config.mysql_pass
app.config['MYSQL_DB'] = config.mysql_db
app.config['MYSQL_PORT'] = config.mysql_port

app.config["DISCORD_CLIENT_ID"] = 962915240071282783 # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "KWgAtKFQPtxAwYZ5ivdTFhhdxnDeaerL" # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://www.gsroleplay.com/auth/discord/callback" # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = "OTYyOTE1MjQwMDcxMjgyNzgz.YlOesw.qfSK7aymWoeJSAUbipeikPW31ZY" # Required to access BOT resources.

# Mercado Pago
app.mercadopago_sdk = mercadopago.SDK(config.MERCADOPAGO_ACCESS_TOKEN)

# Discord
discord = DiscordOAuth2Session(app)

# Check MySQL
try:
	mysql = MySQL(app)
	print(' * [init] MySQL started')

except Exception as e:
	print(f' * [init] MySQL load failed ({e})')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('/info/error.html', code = 404, info = e), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('/info/error.html', code = 500, info = e), 500

# Filters
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.2f}".format(value)

# Auth
from auth.views import auth
app.register_blueprint(auth)

# Info
from info.views import info
app.register_blueprint(info)

# Store
from store.views import store
app.register_blueprint(store)

# Admin
from admin.views import admin
app.register_blueprint(admin)

# Intialize application
if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = config.port, debug = config.debug_mode)
	