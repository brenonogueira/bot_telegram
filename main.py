import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
import logging
from typing import NoReturn
from telegram.error import Forbidden, NetworkError

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TELEGRAM_TOKEN = os.getenv('BOT_TELEGRAM_TOKEN')

async def main() -> NoReturn:
    """Run the bot."""
    # Here we use the `async with` syntax to properly initialize and shutdown resources.
    async with Bot(BOT_TELEGRAM_TOKEN) as bot:
        # get the first pending update_id, this is so we can skip over it in case
        # we get a "Forbidden" exception.
        try:
            update_id = (await bot.get_updates())[0].update_id
        except IndexError:
            update_id = None

        logger.info("listening for new messages...")
        while True:
            try:
                update_id = await echo(bot, update_id)
            except NetworkError:
                await asyncio.sleep(1)
            except Forbidden:
                # The user has removed or blocked the bot.
                update_id += 1


async def echo(bot: Bot, update_id: int) -> int:
    """Echo the message the user sent."""
    # Request updates after the last update_id
    updates = await bot.get_updates(offset=update_id, timeout=10)
    for update in updates:
        next_update_id = update.update_id + 1

        # your bot can receive updates without messages
        # and not all messages contain text
        if update.message and update.message.text:
            # Reply to the message
            logger.info("Found message %s!", update.message.text)
            await update.message.reply_text('hahah')
        return next_update_id
    return update_id


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass
