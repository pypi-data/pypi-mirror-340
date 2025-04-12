"""
Copyright (C) 2025 Литовченко Виктор Иванович (filthps)
Это главный модуль. Класс ORM следует использовать в ваших проектах
"""
import os
from dotenv import load_dotenv
from two_m_root.orm import Main

load_dotenv(os.path.join(os.path.dirname(__file__), "settings.env"))
DATABASE_PATH = os.environ.get("DATABASE_PATH")
MEMCACHE_PATH = os.environ.get("CACHE_PATH")


class ORM(Main):
    CACHE_PATH = MEMCACHE_PATH
    DATABASE_PATH = DATABASE_PATH
    RELEASE_INTERVAL_SECONDS = 5.0
    CACHE_LIFETIME_HOURS = 1 * 60 * 60
