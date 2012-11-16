import irc.bot
import time

class NotifyBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port, text):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.timeout = 1
        self.channel = channel
        self.text = text

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def _on_join(self, c, e):
        irc.bot.SingleServerIRCBot._on_join(self, c,e)
        for line in self.text.split('\n'):
            c.privmsg(self.channel, line)
            time.sleep(0.25)
        self.disconnect()
        self.die()

def notify(header, body, cfg):
    bot = NotifyBot('#'+cfg['IRC.channel'], cfg['IRC.nick'], cfg['IRC.server'], int(cfg['IRC.port']), header+'\n'+body)
    return bot.start()
    