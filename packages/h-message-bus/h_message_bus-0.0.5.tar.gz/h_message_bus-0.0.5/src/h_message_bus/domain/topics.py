from enum import Enum


class Topic(str, Enum):
    """
    Represents a collection of predefined topics as an enumeration.

    This class is an enumeration that defines constant string values for use
    as topic identifiers. These topics represent specific actions or messages
    within a messaging or vector database management context. It ensures
    consistent usage of these predefined topics across the application.

    syntax: [hai].[source].[destination].[action]

    """
    # AI to Telegram
    AI_SEND_TG_CHAT_MESSAGE = "hai.ai.tg.chat.send"

    # AI to vector database
    AI_VECTORS_SAVE = "hai.ai.vectors.save"
    AI_VECTORS_QUERY = "hai.ai.vectors.query"

    # TG to AI
    TG_SEND_AI_CHAT_MESSAGE = "hai.tg.ai.chat.send"
