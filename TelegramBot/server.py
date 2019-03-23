import cherrypy
import json

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers \
        and 'content-type' in cherrypy.request.headers \
        and cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            data = json.loads(json_string)
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

    def start(bot):
        # Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
        bot.remove_webhook()
         # Ставим заново вебхук
        bot.set_webhook(url = config_bot.WEBHOOK_URL_BASE + config_bot.WEBHOOK_URL_PATH,
                        certificate = open(config_bot.WEBHOOK_SSL_CERT, 'r'))
        cherrypy.config.update({
            'server.socket_host': config_bot.WEBHOOK_LISTEN,
            'server.socket_port': config_bot.WEBHOOK_PORT,
            'server.ssl_module': 'builtin',
            'server.ssl_certificate': config_bot.WEBHOOK_SSL_CERT,
            'server.ssl_private_key': config_bot.WEBHOOK_SSL_PRIV
        })
        #запуск сервера
        cherrypy.quickstart(WebhookServer(), config_bot.WEBHOOK_URL_PATH, {'/': {}})
