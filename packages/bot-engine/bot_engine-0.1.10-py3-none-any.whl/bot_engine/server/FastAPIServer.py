from os import getenv
from threading import Thread

import uvicorn

from keyboard import add_hotkey
from fastapi import FastAPI
from contextlib import asynccontextmanager

if getenv("ENVIRONMENT") == "testing":
    from data.env import ENVIRONMENT
    from bot.Bot import Bot

else:
    from bot_engine.data.env import ENVIRONMENT
    from bot_engine.bot.Bot import Bot


class FastAPIServer:
    """FastAPI server. You can easily extend it with your needs"""

    def __init__(self, bot: Bot = None):
        """constructor needs bot instance to run"""
        # threads to run things concurrently
        self.bot_thread: Thread = None
        self.hotkey_listener_thread: Thread = None

        self.bot = bot or Bot()
        self.app = FastAPI(lifespan=self.start_server)

    @asynccontextmanager
    async def start_server(self, app: FastAPI):
        print("сервер FastAPI / uvicorn включён 👀")
        self.start_threads()

        try:
            yield

        except KeyboardInterrupt:
            print("Manual shutdown triggered.")

        finally:
            self.shut_server_down()

    def start_threads(self):
        if ENVIRONMENT == "development" or ENVIRONMENT == "testing":
            self.listen_to_ctrl_c_thread()

        if ENVIRONMENT == "production":
            pass

        self.start_bot_thread()

    def start_bot_thread(self):
        """
        Things you run on a server startup.
        For example, run neccessary bot components to work

        1. Run DB
            database = Database()
            database.sync_cache_and_remote_users()

        2. Prepare some intermediary stuff like scheduling
            database.mongoDB.ScheduleDays.check_days_integrity()

        3. Run bot components, like dialogs, filters etc
            BotDialogs().enable_dialogs()

        3. Last one: start your bot
        #? start bot
        # self.bot_thread = Thread(target=self.bot.start)
        # self.bot_thread.start()
        """
        self.bot_thread = Thread(target=self.bot.start)
        self.bot_thread.start()

    def listen_to_ctrl_c_thread(self):
        self.hotkey_listener_thread = Thread(target=self.handle_ctrl_c)
        self.hotkey_listener_thread.start()

    def handle_ctrl_c(self):
        add_hotkey("ctrl+c", self.shut_server_down)

    def shut_server_down(self):
        """
        Things to run when server is shutting down.

        For example:

        self.bot.disconnect()
        uvicorn.server.Server.should_exit = True

        if ENVIRONMENT == "development" or ENVIRONMENT == "testing":
            self.hotkey_listener_thread.join()

        if ENVIRONMENT == "production":
            pass

        self.bot_thread.join()
        print("Сервер выключен ❌")

        """
        self.bot.disconnect()
        uvicorn.server.Server.should_exit = True

        if ENVIRONMENT == "development" or ENVIRONMENT == "testing":
            self.hotkey_listener_thread.join()

        if ENVIRONMENT == "production":
            pass

        self.bot_thread.join()
        print("Сервер выключен ❌")
