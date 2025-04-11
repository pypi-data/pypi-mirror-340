from tgram_dnd.flows import MessageFlow, CallbackFlow
from tgram_dnd.caching.base import BaseCache
from tgram_dnd.caching.memory import MemoryCache
from tgram_dnd.config import BotConfig

from tgram import TgBot

from typing import List, Union

class App:
    '''The main class used to run your Flows'''
    def __init__(
        self,
        bot: TgBot,
        flows: List[Union[MessageFlow, CallbackFlow]] = [],
        config: BotConfig = None,
        cache: BaseCache = None
    ):
        self.bot = bot
        self.flows = flows
        self.config = config
        self.cache = cache or MemoryCache()

    def add_flows(
        self,
        flows: Union[List[Union[MessageFlow, CallbackFlow]], Union[MessageFlow, CallbackFlow]]
    ):
        '''add flows to current app'''
        flows = [flows] if not isinstance(flows, list) else flows
        self.flows += flows
    
    def run(self) -> None:
        '''run the bot'''
        for flow in self.flows:
            flow.inject(self)
            flow.load_plugin()
        
        # setting up config
        if self.config:
            self.config.configure(bot=self.bot)

        self.bot.run()