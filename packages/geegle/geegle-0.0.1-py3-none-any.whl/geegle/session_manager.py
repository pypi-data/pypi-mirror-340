import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Any

class SessionManager:    
    def __init__(self):
        home_dir = Path.home()
        self.sessions_dir = home_dir / ".geegle" / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = self.sessions_dir / "sessions.db"
        self.sessions = {}
        self.current_session = "default"
        self.db = None
    
    async def init(self):
        self.db = sqlite3.connect(self.db_path)
        self._create_table_if_not_exists()
        self._load_sessions()
    
    def _create_table_if_not_exists(self):
        cursor = self.db.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            name TEXT PRIMARY KEY,
            history TEXT
        )
        ''')
        self.db.commit()
    
    def _load_sessions(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT name, history FROM sessions')
        rows = cursor.fetchall()
        
        for name, history in rows:
            self.sessions[name] = json.loads(history)
        
        if "default" not in self.sessions:
            self.sessions["default"] = []
            self._save_session("default")
    
    def _save_session(self, session_name: str):
        history_json = json.dumps(self.sessions.get(session_name, []))
        cursor = self.db.cursor()
        cursor.execute(
            'INSERT OR REPLACE INTO sessions (name, history) VALUES (?, ?)',
            (session_name, history_json)
        )
        self.db.commit()
    
    def get_current_session(self) -> str:
        return self.current_session
    
    def get_session_history(self) -> List[Dict[str, Any]]:
        return self.sessions.get(self.current_session, [])
    
    def update_session_history(self, history: List[Dict[str, Any]]):
        self.sessions[self.current_session] = history
        self._save_session(self.current_session)
    
    def list_sessions(self) -> List[str]:
        return list(self.sessions.keys())
    
    def switch_session(self, session_name: str) -> bool:
        if session_name not in self.sessions:
            self.sessions[session_name] = []
            self._save_session(session_name)
        
        self.current_session = session_name
        return True
    
    def delete_session(self, session_name: str) -> bool:
        if session_name == "default":
            return False
        
        if session_name in self.sessions:
            del self.sessions[session_name]
            
            cursor = self.db.cursor()
            cursor.execute('DELETE FROM sessions WHERE name = ?', (session_name,))
            self.db.commit()
            
            if self.current_session == session_name:
                self.current_session = "default"
           
            return True
        
        return False
    
    async def clear_all_sessions(self):
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM sessions')
        self.db.commit()
        
        self.sessions.clear()
        self.sessions["default"] = []
        self.current_session = "default"
        self._save_session("default")
    
    async def export_sessions(self, filename: str):
        all_sessions = {}
        
        cursor = self.db.cursor()
        cursor.execute('SELECT name, history FROM sessions')
        rows = cursor.fetchall()
        
        for name, history in rows:
            all_sessions[name] = json.loads(history)
        
        with open(filename, 'w') as f:
            json.dump(all_sessions, f, indent=2)