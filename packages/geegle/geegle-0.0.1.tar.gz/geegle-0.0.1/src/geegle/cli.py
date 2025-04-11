from typing import List
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from rich.console import Console
from rich.theme import Theme
from pathlib import Path

from geegle.chat_service import ChatService
from geegle.session_manager import SessionManager

class CLI:    
    def __init__(self):
        self.session_manager = SessionManager()
        self.chat_service = ChatService(self.session_manager)
        
        self.console = Console(theme=Theme({
            "info": "cyan",
            "warning": "yellow",
            "error": "red",
            "success": "green"
        }))
        
        history_file = Path.home() / ".geegle" / "command_history.txt"
        history_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.prompt_style = Style.from_dict({
            'prompt': '#00aa00 bold',
        })
        
        self.session = PromptSession(
            history=FileHistory(str(history_file))
        )
    
    async def start(self):
        await self.session_manager.init()
        
        self.console.print("\n===== Geegle Chat with Web Search & Sessions =====")
        self.console.print("Type your question and press Enter. Type \"exit\" to quit.")
        self.console.print("Commands: /clear, /clear all, /export sessions, /session, /help\n")
        
        while True:
            try:
                prompt_text = HTML(f'<prompt>{self.chat_service.get_current_session()}></prompt> ')
                
                user_input = await self.session.prompt_async(
                    prompt_text,
                    style=self.prompt_style
                )
                
                if not user_input:
                    continue
                
                user_input = user_input.strip()
                
                if user_input.lower() == "exit":
                    break
                
                if user_input.startswith("/"):
                    await self.handle_command(user_input)
                else:
                    self.console.print("\nThinking...")
                    await self.chat_service.chat(user_input)
                    self.console.print("\nDone! Ask another question or type exit to quit.")
            
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                self.console.print(f"\n[error]Error: {str(e)}[/error]")
                self.console.print("Please try again or check your API keys if the error persists.")
        
        self.console.print("\nThank you for using Geegle! Goodbye!\n")
    
    async def handle_command(self, input_text: str):
        parts = input_text.split(" ")
        command = parts[0]
        args = parts[1:]
        
        if command == "/clear":
            if args and args[0] == "all":
                self.console.print("[error]\nWARNING: This will delete all session data permanently.[/error]")
                self.console.print("[warning]Make sure you have exported your sessions if you want to keep a backup.[/warning]")
                
                confirm = await self.confirm_clear_all()
                if confirm:
                    await self.session_manager.clear_all_sessions()
                else:
                    self.console.print("Operation canceled.")
            else:
                self.chat_service.clear_history()
                self.console.print("Conversation history cleared.")
        
        elif command == "/export":
            if args and args[0] == "sessions":
                filename = args[1] if len(args) > 1 else "sessions_export.json"
                await self.session_manager.export_sessions(filename)
                self.console.print(f"[success]Sessions exported to {filename}[/success]")
            else:
                self.console.print("Usage: /export sessions [filename]")
        
        elif command == "/help":
            self.display_help()
        
        elif command == "/session":
            await self.handle_session_command(args)
        
        else:
            self.console.print(f"Unknown command: {command}. Type /help for available commands.")
    
    async def confirm_clear_all(self) -> bool:
        prompt_text = HTML("<prompt>Are you sure you want to clear all session data? Type \"yes\" to confirm: </prompt>")
        
        answer = await self.session.prompt_async(prompt_text, style=self.prompt_style)
        return answer.lower() == "yes"
    
    def display_help(self):
        self.console.print("\n===== Geegle Help =====")
        self.console.print("- Ask any question to get an answer with web sources")
        self.console.print("- Type /clear to clear current session history")
        self.console.print("- Type /clear all to clear all session data (requires confirmation)")
        self.console.print("- Type /export sessions [filename] to export all sessions to a JSON file")
        self.console.print("- Type /session new <name> to create a new session")
        self.console.print("- Type /session list to see all available sessions")
        self.console.print("- Type /session switch <name> to switch to a different session")
        self.console.print("- Type /session delete <name> to delete a session")
        self.console.print("- Type exit to quit the application\n")
    
    async def handle_session_command(self, args: List[str]):
        if not args:
            self.console.print(f"Current session: {self.chat_service.get_current_session()}")
            return
        
        action = args[0]
        
        if action == "list":
            sessions = self.chat_service.list_sessions()
            current = self.chat_service.get_current_session()
            
            self.console.print("\nAvailable sessions:")
            for session in sessions:
                indicator = "* " if session == current else "  "
                self.console.print(f"{indicator}{session}")
            self.console.print("")
        
        elif action in ["new", "switch"]:
            if len(args) < 2:
                self.console.print(f"Please provide a session name for {action}.")
                return
            
            session_name = args[1]
            if await self.chat_service.switch_session(session_name):
                self.console.print(f"[success]Switched to session: {session_name}[/success]")
            else:
                self.console.print(f"[error]Failed to switch to session: {session_name}[/error]")
        
        elif action == "delete":
            if len(args) < 2:
                self.console.print("Please provide a session name to delete.")
                return
            
            session_to_delete = args[1]
            if session_to_delete == "default":
                self.console.print("[error]Cannot delete the default session.[/error]")
                return
            
            if await self.chat_service.delete_session(session_to_delete):
                self.console.print(f"[success]Deleted session: {session_to_delete}[/success]")
            else:
                self.console.print(f"[error]Failed to delete session: {session_to_delete}[/error]")
        
        else:
            self.console.print(f"Unknown session command: {action}. Type /help for usage.")