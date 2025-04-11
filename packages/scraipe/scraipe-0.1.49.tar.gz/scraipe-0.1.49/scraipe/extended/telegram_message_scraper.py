import telethon.client
import telethon.sessions
from scraipe.classes import IScraper, ScrapeResult
import requests
from bs4 import BeautifulSoup
import re
from scraipe.async_classes import IAsyncScraper
from scraipe.async_util import AsyncManager
import warnings

from telethon import TelegramClient
from telethon.sessions import StringSession, SQLiteSession
from threading import Lock
import telethon

import logging
from sqlite3 import OperationalError

class TelegramMessageScraper(IAsyncScraper):
    """
    A scraper that uses the telethon library to pull the contents of Telegram messages.

    Attributes:
        api_id (str): The API ID for the Telegram client.
        api_hash (str): The API hash for the Telegram client.
        phone_number (str): The phone number associated with the Telegram account.

    """
        
    DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

    def __init__(self, api_id: str, api_hash: str, phone_number: str, session_name:str = None, sync_auth: bool = True):
        """
        Initialize the TelegramMessageScraper with necessary connection parameters.

        Parameters:
            api_id (str): The Telegram API ID.
            api_hash (str): The Telegram API hash.
            phone_number (str): The phone number for authentication.
            session_name (str): The name of the session. If None, a temporary StringSesssion will be used 
        """
        self.session_name = session_name
        self.session_string = None
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.session_lock = Lock()
        
        logging.info(f"Initializing the Telegram session...")
        if not self.authenticate(sync_auth):
            raise RuntimeError("Failed to authenticate the Telegram session. Please check your credentials.")
    
    def save_session(self, client:TelegramClient):
        with self.session_lock:
            # Serialize a session for creating new clients
            self.session_string = StringSession.save(client.session)
            logging.info("Successfully authenticated.")
    
    async def _sign_in(self, phone_number: str, code: str, phone_code_hash: str, client: TelegramClient = None, password:str = None):
        password = None if password == "" else password        
                
        if client is None:
            client = TelegramClient(self.session_name, api_id=self.api_id, api_hash=self.api_hash)
            
        await client.connect()
        if not await client.is_user_authorized():
            try:
                await client.sign_in(phone=phone_number, code=code, phone_code_hash=phone_code_hash, password=password)
            except telethon.errors.SessionPasswordNeededError as e:
                if password is None:
                    logging.warning("Two-factor authentication is enabled. Please enter your password.")
                raise e
            
            if await client.is_user_authorized():
                self.save_session(client)
            else:
                logging.warning("Failed to authenticate. Please check your credentials.")
        else:
            logging.info("Already authenticated. No need to sign in.")
        
    
    def sign_in(self, phone_number: str, code: str, phone_code_hash: str, password:str = None):
        """
        Sign in to the Telegram account using the provided phone number, code, and password.

        Parameters:
            phone_number (str): The phone number associated with the account.
            code (str): The verification code sent to the phone number.
            phone_code_hash (str): The hash of the verification code.
            password (str): The password for two-factor authentication, if enabled.

        Raises:
            telethon.errors.SessionPasswordNeededError: If two-factor authentication is enabled and no password is provided.
        """
        AsyncManager.get_executor().run(self._sign_in(phone_number, code, phone_code_hash, password=password))
        
    def authenticate(self, sync_auth = True) -> bool:
        """
        Authenticate the Telegram session and return whether the authentication was successful.
        """
        async def _authenticate():
            try:
                try:
                    client = TelegramClient(self.session_name, api_id=self.api_id, api_hash=self.api_hash)
                except Exception as e:
                    logging.warning(f"Failed to acquire SQLite session. Creating a temporary StringSession.")
                    client = TelegramClient(StringSession(), api_id=self.api_id, api_hash=self.api_hash)

                is_authd = False
                
                await client.connect()
                if await client.is_user_authorized():
                    logging.info("Already authenticated. No need to authenticate again.")
                    is_authd = True
                else:
                    sent = await client.send_code_request(phone=self.phone_number)
                    phone_code_hash = sent.phone_code_hash

                    if sync_auth:
                        # get input from user and sign in immediately
                        code = input("Enter the code you received: ")
                        try:
                            await self._sign_in(self.phone_number, code, phone_code_hash, client)
                        except telethon.errors.SessionPasswordNeededError:
                            password = input("Two-factor authentication is enabled. Please enter your password: ")
                            await self._sign_in(self.phone_number, code, phone_code_hash, client, password)              
                    is_authd = await client.is_user_authorized()
                await client.disconnect()
                    
                if is_authd: 
                    self.save_session(client)
                    return True
                else:
                    logging.warning("Not authenticated. Please check your credentials.")
                    return False
            except Exception as e:
                import traceback
                logging.error(f"Failed to authenticate due to exception: {e}")
                return False
            else:
                return True
        return AsyncManager._executor.run(_authenticate())
        
    def get_expected_link_format(self):
        # regex for telegram message links
        return "https://t.me/[^/]+/[0-9]+"

    async def _get_telegram_content(self, chat_name: str, message_id: int):
        """
        Retrieve the content of a Telegram message asynchronously.

        Parameters:
            chat_name (str): The username or ID of the chat.
            message_id (int): The ID of the message to retrieve.

        Returns:
            str: The text or caption of the Telegram message.

        Raises:
            Exception: If failing to retrieve the chat or message, or if the chat is restricted.
        """
        assert self.session_string is not None, "Session is None. Please authenticate first."
        client = TelegramClient(StringSession(self.session_string), api_id=self.api_id, api_hash=self.api_hash)
        await client.connect()
        if not await client.is_user_authorized():
            raise Exception("Telagram session not auth'd. Please authenticate by calling authenticate().")        
        async with client:        
            # Get chat
            try:
                entity = await client.get_entity(chat_name)
            except Exception as e:
                raise Exception(f"Failed to get chat for {chat_name}: {e}")
            if hasattr(entity, 'restricted') and entity.restricted:
                raise Exception(f"Chat {chat_name} is restricted.")
            
            # get message
            try:
                message = await client.get_messages(entity,ids=message_id)
            except Exception as e:
                raise Exception(f"Failed to get message {message_id} from {chat_name}: {e}")
            
            # Extract content
            if message is None:
                raise Exception(f"Message {message_id} from {chat_name} is None.")
            if message.message is not None:
                content = message.message
            else:
                raise Exception(f"Message {message_id} from {chat_name} is None.")
            return content

    async def async_scrape(self, url: str) -> ScrapeResult:
        """
        Asynchronously scrape the content of a Telegram message from a URL.

        Parameters:
            url (str): A URL formatted as 'https://t.me/{username}/{message_id}'.

        Returns:
            ScrapeResult: An object representing the success or failure of the scraping process.

        The method validates the URL, extracts the username and message ID, and retrieves the message content.
        """
        if not url.startswith("https://t.me/"):
            return ScrapeResult(link=url, scrape_success=False, scrape_error=f"URL {url} is not a telegram link.")
        match = re.match(r"https://t.me/([^/]+)/(\d+)", url)
        if not match:
            error = f"Failed to extract username and message id from {url}"
            return ScrapeResult.fail(url, error)
        username, message_id = match.groups()
        try:
            message_id = int(message_id)
        except ValueError:
            error = f"Message ID {message_id} is not a valid integer."
            return ScrapeResult.fail(url, error)
        try:
            content = await self._get_telegram_content(username, message_id)
            assert content is not None, f"Message {message_id} from {username} is None."
        except Exception as e:
            return ScrapeResult.fail(url, f"Failed to scrape due to exception: {e}")
        return ScrapeResult.succeed(url, content)

    def disconnect(self):
        """
        Disconnect any active sessions or clean up resources.

        Note:
            This method is currently a placeholder with no implemented disconnect logic.
        """
        pass