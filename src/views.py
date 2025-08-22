import json
import requests
from datetime import datetime, timedelta
import pandas as pd
import os

def greeting() -> str:
    """Приветствует пользователя с учетом времени суток"""
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"
