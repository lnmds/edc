import logging
import sys
import asyncio

from PyQt5.QtWidgets import QApplication, QProgressBar, \
        QMessageBox, QLineEdit
from quamash import QEventLoop

from .bot import Client

logging.basicConfig(level=logging.INFO)

app = QApplication(sys.argv)
loop = QEventLoop(app)
asyncio.set_event_loop(loop)

progress = QProgressBar()
progress.setRange(0, 100)
progress.show()

async def main(config):
    app.init_task = loop.create_task(init_screen())

    bot = Client(loop=loop,
                 command_prefix='demon ',
                 ready_callback=ready)
    app.bot = bot

    @bot.command()
    async def ping(ctx):
        await ctx.send('hello')

    loop.create_task(bot.start(config.TOKEN))


async def ready(bot):
    app.init_task.cancel()
    progress.setValue(100)

    box = QMessageBox()
    box.setText(f'{bot.user} is ready!')
    box.exec()

    # send msg
    app.message_line = QLineEdit()
    app.message_line.show()
    app.message_line.connect(send_text)

async def send_text():
    text = app.message_line.text()
    chan = app.bot.get_channel(366746609041801227)
    await chan.send(text)


async def init_screen():
    for i in range(101):
        progress.setValue(i)
        await asyncio.sleep(.12)


def run(config):
    with loop:
        loop.create_task(main(config))
        loop.run_forever()
