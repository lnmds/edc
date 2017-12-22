import logging

from discord.ext import commands

log = logging.getLogger(__name__)


class Client(commands.Bot):
    """Main client class."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ready_callback = kwargs.get('ready_callback')
    
    async def on_ready(self):
        log.info('calling ready callback')
        await self.ready_callback(self)
