import json
import sqlite3
import time
from pathlib import Path
from typing import Dict, Any, Optional

class CacheService:
    def __init__(self):
        home_dir = Path.home()
        self.cache_dir = home_dir / ".geegle" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = self.cache_dir / "search_cache.db"
        self.db = None
        self.max_cache_age = 7 * 24 * 60 * 60
    
    async def init(self):
        self.db = sqlite3.connect(self.db_path)
        self._create_tables_if_not_exist()
    
    def _create_tables_if_not_exist(self):
        cursor = self.db.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_cache (
            query TEXT PRIMARY KEY,
            service TEXT,
            response TEXT,
            timestamp INTEGER
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS webpage_cache (
            url TEXT PRIMARY KEY,
            content TEXT,
            timestamp INTEGER
        )
        ''')
        
        self.db.commit()
    
    async def get_cached_search(self, query: str, service: str) -> Optional[Dict[str, Any]]:
        if not self.db:
            await self.init()
            
        cursor = self.db.cursor()
        cursor.execute(
            'SELECT response, timestamp FROM search_cache WHERE query = ? AND service = ?',
            (query, service)
        )
        
        result = cursor.fetchone()
        if not result:
            return None
            
        response_json, timestamp = result
        
        if time.time() - timestamp > self.max_cache_age:
            return None
            
        try:
            return json.loads(response_json)
        except json.JSONDecodeError:
            return None
    
    async def cache_search_results(self, query: str, service: str, results: Dict[str, Any]):
        if not self.db:
            await self.init()
            
        cursor = self.db.cursor()
        cursor.execute(
            'INSERT OR REPLACE INTO search_cache (query, service, response, timestamp) VALUES (?, ?, ?, ?)',
            (query, service, json.dumps(results), int(time.time()))
        )
        self.db.commit()
    
    async def get_cached_webpage(self, url: str) -> Optional[Dict[str, Any]]:
        if not self.db:
            await self.init()
            
        cursor = self.db.cursor()
        cursor.execute('SELECT content, timestamp FROM webpage_cache WHERE url = ?', (url,))
        
        result = cursor.fetchone()
        if not result:
            return None
            
        content_json, timestamp = result
        
        if time.time() - timestamp > self.max_cache_age:
            return None
            
        try:
            return json.loads(content_json)
        except json.JSONDecodeError:
            return None
        
    async def cache_webpage(self, url: str, content: Dict[str, Any]):
        if not self.db:
            await self.init()
            
        cursor = self.db.cursor()
        cursor.execute(
            'INSERT OR REPLACE INTO webpage_cache (url, content, timestamp) VALUES (?, ?, ?)',
            (url, json.dumps(content), int(time.time()))
        )
        self.db.commit()
    
    async def clear_cache(self):
        if not self.db:
            await self.init()
            
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM search_cache')
        cursor.execute('DELETE FROM webpage_cache')
        self.db.commit()