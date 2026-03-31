import os
import re
import json
import logging
import requests
import time
import random
from datetime import datetime
from typing import Optional  # <-- ВАЖНО: добавлен этот импорт!
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

from database import ArticlesDatabase

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

USE_OPENROUTER = True
OPENROUTER_MODEL = "deepseek/deepseek-chat-v3-0324:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

db = ArticlesDatabase()

stats = {
    "users": set(),
    "requests": 0,
    "openrouter_requests": 0,
    "start_time": datetime.now()
}

class OpenRouterClient:

    def __init__(self, api_key: str, model: str = OPENROUTER_MODEL):
        self.api_key = api_key
        self.model = model
        self.base_url = OPENROUTER_URL

    def generate_response(self, prompt: str, context: str, max_tokens: int = 1000) -> Optional[str]:

        if not self.api_key:
            logger.error("OpenRouter API ключ не задан")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yourusername/eco_bot",
            "X-Title": "Eco Legal Assistant"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": """Ты - юридический ассистент, специализирующийся на экологических правонарушениях (КоАП РФ). 
Отвечай ТОЛЬКО на основе предоставленных статей. 
Если информация отсутствует в контексте, честно скажи об этом.
Форматируй ответы понятно для обычных людей, используй эмодзи для наглядности.
Не придумывай статьи и штрафы, которых нет в контексте."""
                },
                {
                    "role": "user",
                    "content": f"Контекст (статьи КоАП РФ):\n{context}\n\nВопрос пользователя: {prompt}"
                }
            ],
            "temperature": 0.1,
            "max_tokens": max_tokens
        }

        # Пробуем несколько раз с задержкой
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"Повторная попытка {attempt + 1} через {wait_time:.1f} сек...")
                    time.sleep(wait_time)

                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()
                    if "choices" in data and len(data["choices"]) > 0:
                        return data["choices"][0]["message"]["content"]
                    else:
                        logger.error(f"Неожиданный формат ответа: {data}")
                        return None

                elif response.status_code == 401:
                    logger.error("Ошибка авторизации OpenRouter: неверный API ключ")
                    return None

                elif response.status_code == 402:
                    logger.error("Требуется оплата на OpenRouter")
                    return None

                elif response.status_code == 429:
                    logger.warning(f"Rate limit превышен (попытка {attempt + 1})")
                    if attempt < max_retries - 1:
                        continue
                    else:
                        return None

                elif response.status_code >= 500:
                    logger.warning(f"Серверная ошибка {response.status_code} (попытка {attempt + 1})")
                    if attempt < max_retries - 1:
                        continue
                    else:
                        return None

                else:
                    logger.error(f"Ошибка {response.status_code}: {response.text[:200]}")
                    return None

            except requests.exceptions.Timeout:
                logger.warning(f"Таймаут (попытка {attempt + 1})")
                if attempt == max_retries - 1:
                    return None

            except requests.exceptions.ConnectionError:
                logger.warning(f"Ошибка подключения (попытка {attempt + 1})")
                if attempt == max_retries - 1:
                    return None

            except Exception as e:
                logger.error(f"Неожиданная ошибка: {e}")
                return None

        return None