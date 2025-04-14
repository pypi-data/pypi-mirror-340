import openai
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.completion import Completer, Completion
from rich.console import Console
from rich.theme import Theme
from pathlib import Path
from rich.panel import Panel
import getpass
import os
import re
import time

from geegle.chat_service import ChatService
from geegle.session_manager import SessionManager

class GeegleCompleter(Completer):
    def __init__(self, chat_service):
        self.chat_service = chat_service
        self.base_commands = [
            "/clear", "/clear all", "/export", "/help", 
            "/session", "/model", "/prompt"
        ]
    
    def get_completions(self, document, complete_event):
        text = document.text
        
        if not text or text.startswith("/") and " " not in text:
            word_before_cursor = document.get_word_before_cursor()
            for command in self.base_commands:
                if command.startswith(word_before_cursor):
                    yield Completion(
                        command, 
                        start_position=-len(word_before_cursor)
                    )
        
        elif text.startswith("/"):
            command, *args = text.split(" ", 1)
            arg = args[0] if args else ""
            
            if command == "/session":
                for session in self.chat_service.list_sessions():
                    if session.startswith(arg):
                        yield Completion(
                            session,
                            start_position=-len(arg)
                        )
            
            elif command == "/model":
                for model in self.chat_service.config.AVAILABLE_MODELS:
                    if model.startswith(arg):
                        yield Completion(
                            model,
                            start_position=-len(arg)
                        )
            
            elif command == "/prompt":
                for template in self.chat_service.config.PROMPT_TEMPLATES:
                    if template.startswith(arg):
                        yield Completion(
                            template,
                            start_position=-len(arg)
                        )

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
        
        self.completer = GeegleCompleter(self.chat_service)
        
        self.session = PromptSession(
            history=FileHistory(str(history_file)),
            completer=self.completer
        )
    
    async def start(self):
        await self.session_manager.init()
        
        self.console.print("\n===== Geegle Chat with Web Search & Sessions =====")
        self.console.print("Type your question and press Enter. Type \"exit\" to quit.")
        self.console.print("Commands: /clear, /session, /model, /prompt, /help\n")
        
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
        parts = input_text.split(" ", 1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        
        if command == "/clear":
            if args == "all":
                self.console.print("[error]\nWARNING: This will delete all session data permanently.[/error]")
                self.console.print("[warning]Make sure you have exported your sessions if you want to keep a backup.[/warning]")
                
                confirm = await self.confirm_clear_all()
                if confirm:
                    await self.session_manager.clear_all_sessions()
                    self.console.print("[success]All sessions cleared.[/success]")
                else:
                    self.console.print("Operation canceled.")
            else:
                self.chat_service.clear_history()
                self.console.print("[success]Conversation history cleared.[/success]")
        
        elif command == "/export":
            raw_filename = args.strip() if args else "sessions_export.json"
            
            safe_filename = os.path.basename(raw_filename)
            
            exports_dir = Path.home() / ".geegle" / "exports"
            exports_dir.mkdir(parents=True, exist_ok=True)
            
            if safe_filename != raw_filename:
                self.console.print(f"[warning]Path elements detected in filename.[/warning]")
                self.console.print(f"[warning]Original: '{raw_filename}'[/warning]")
                self.console.print(f"[warning]Using safe filename: '{safe_filename}'[/warning]")
            
            def is_safe_filename_content(filename):
                return bool(re.match(r'^[a-zA-Z0-9_\-\.]+$', filename))
                
            if not is_safe_filename_content(safe_filename):
                safe_filename = f"export_{int(time.time())}.json"
                self.console.print(f"[warning]Invalid characters in filename.[/warning]")
                self.console.print(f"[warning]Using generated filename: {safe_filename}[/warning]")
            
            export_path = exports_dir / safe_filename
            
            await self.session_manager.export_sessions(str(export_path))
            
            self.console.print(f"[success]Sessions successfully exported![/success]")
            self.console.print(f"[info]Location: {export_path}[/info]")
            
            self.console.print("\n[info]To access your export file, you can find it at:[/info]")
            self.console.print(f"[info]{exports_dir}[/info]")
        
        elif command == "/rerank":
            if not args:
                status = "enabled" if self.chat_service.config.USE_RERANKER else "disabled"
                self.console.print(f"Reranker is currently {status}")
            else:
                arg = args.strip().lower()
                if arg == "on":
                    self.chat_service.config.USE_RERANKER = True
                    self.chat_service.config._save_config()
                    self.console.print("[success]Reranker enabled[/success]")
                elif arg == "off":
                    self.chat_service.config.USE_RERANKER = False
                    self.chat_service.config._save_config()
                    self.console.print("[success]Reranker disabled[/success]")
                else:
                    self.console.print("[error]Usage: /rerank [on|off][/error]")
        
        elif command == "/help":
            self.display_help()
        
        elif command == "/session":
            if not args:
                await self.display_session_menu()
            else:
                session_name = args.strip()
                if await self.chat_service.switch_session(session_name):
                    self.console.print(f"[success]Switched to session: {session_name}[/success]")
                else:
                    self.console.print(f"[error]Failed to switch to session: {session_name}[/error]")
        
        elif command == "/model":
            if not args:
                await self.display_model_menu()
            else:
                model_name = args.strip()
                if self.chat_service.config.set_model(model_name):
                    self.console.print(f"[success]Model set to: {model_name}[/success]")
                else:
                    self.console.print(f"[error]Invalid model: {model_name}. Use '/model' to see available models.[/error]")
        
        elif command == "/prompt":
            if not args:
                await self.display_prompt_menu()
            else:
                if args.strip() in self.chat_service.config.PROMPT_TEMPLATES:
                    template_name = args.strip()
                    if self.chat_service.config.use_prompt_template(template_name):
                        self.console.print(f"[success]Now using prompt template: {template_name}[/success]")
                else:
                    new_prompt = args.strip()
                    self.chat_service.config.update_system_prompt(new_prompt)
                    self.console.print(f"[success]System prompt updated.[/success]")
        
        else:
            self.console.print(f"Unknown command: {command}. Type /help for available commands.")

    async def display_session_menu(self):
        """Display an interactive menu for session management."""
        sessions = self.chat_service.list_sessions()
        current = self.chat_service.get_current_session()
        
        self.console.print("\n[bold]Session Management[/bold]")
        self.console.print("Current session: " + current)
        self.console.print("\nAvailable sessions:")
        
        for i, session in enumerate(sessions, 1):
            indicator = "* " if session == current else "  "
            self.console.print(f"{i}. {indicator}{session}")
        
        self.console.print("\n[bold]Options:[/bold]")
        self.console.print("n - Create new session")
        self.console.print("d - Delete a session")
        self.console.print("1-{} - Switch to session".format(len(sessions)))
        self.console.print("q - Return to chat")
        
        choice = await self.session.prompt_async("Enter choice: ")
        
        if choice.lower() == 'n':
            new_session = await self.session.prompt_async("Enter new session name: ")
            if new_session.strip():
                if await self.chat_service.switch_session(new_session.strip()):
                    self.console.print(f"[success]Created and switched to session: {new_session}[/success]")
        
        elif choice.lower() == 'd':
            del_session = await self.session.prompt_async("Enter session number to delete: ")
            try:
                idx = int(del_session) - 1
                if 0 <= idx < len(sessions):
                    session_to_delete = sessions[idx]
                    if session_to_delete != "default":
                        if await self.chat_service.delete_session(session_to_delete):
                            self.console.print(f"[success]Deleted session: {session_to_delete}[/success]")
                    else:
                        self.console.print("[error]Cannot delete the default session.[/error]")
            except ValueError:
                self.console.print("[error]Please enter a valid session number.[/error]")
        
        elif choice.isdigit():
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(sessions):
                    if await self.chat_service.switch_session(sessions[idx]):
                        self.console.print(f"[success]Switched to session: {sessions[idx]}[/success]")
            except ValueError:
                self.console.print("[error]Please enter a valid session number.[/error]")

    async def display_model_menu(self):
        """Display an interactive menu for model selection."""
        models = self.chat_service.config.AVAILABLE_MODELS
        current = self.chat_service.config.DEFAULT_MODEL
        
        self.console.print("\n[bold]Model Selection[/bold]")
        self.console.print("Current model: " + current)
        self.console.print("\nAvailable models:")
        
        for i, model in enumerate(models, 1):
            indicator = "* " if model == current else "  "
            
            provider = self.chat_service.config.get_model_provider(model)
            has_key = self.chat_service.config.has_required_api_key(model)
            
            if not has_key:
                self.console.print(f"{i}. {indicator}{model} [yellow](requires {provider} API key)[/yellow]")
            else:
                self.console.print(f"{i}. {indicator}{model}")
        
        self.console.print("\n[bold]Options:[/bold]")
        self.console.print("1-{} - Select model".format(len(models)))
        self.console.print("a - Add custom model")
        self.console.print("r - Remove a model")
        self.console.print("k - Manage API keys")
        self.console.print("q - Return to chat")
        
        choice = await self.session.prompt_async("Enter choice: ")
        
        if choice.lower() == 'k':
            await self.display_api_key_menu()
        
        if choice.lower() == 'a':
            new_model = await self.session.prompt_async("Enter model name: ")
            if new_model.strip():
                if new_model.strip() not in models:
                    self.chat_service.config.AVAILABLE_MODELS.append(new_model.strip())
                    self.chat_service.config._save_config()
                    self.console.print(f"[success]Added model: {new_model}[/success]")
                else:
                    self.console.print("[warning]Model already exists.[/warning]")
        
        elif choice.lower() == 'r':
            del_model = await self.session.prompt_async("Enter model number to remove: ")
            try:
                idx = int(del_model) - 1
                if 0 <= idx < len(models):
                    model_to_delete = models[idx]
                    if model_to_delete != current:
                        self.chat_service.config.AVAILABLE_MODELS.remove(model_to_delete)
                        self.chat_service.config._save_config()
                        self.console.print(f"[success]Removed model: {model_to_delete}[/success]")
                    else:
                        self.console.print("[error]Cannot remove the current model.[/error]")
            except ValueError:
                self.console.print("[error]Please enter a valid model number.[/error]")
        
        elif choice.isdigit():
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(models):
                    model_name = models[idx]
                    provider = self.chat_service.config.get_model_provider(model_name)
                    has_key = self.chat_service.config.has_required_api_key(model_name)
                    
                    if not has_key:
                        if provider == "anthropic":
                            self.console.print("[yellow]This model requires an Anthropic API key.[/yellow]")
                            api_key = await self.session.prompt_async("Enter your Anthropic API key (or press Enter to cancel): ")
                            
                            if api_key.strip():
                                self.chat_service.config.ANTHROPIC_API_KEY = api_key.strip()
                                self.chat_service.config._save_config()
                                
                                if not hasattr(self.chat_service, 'anthropic_client') or not self.chat_service.anthropic_client:
                                    try:
                                        from anthropic import Anthropic
                                        self.chat_service.anthropic_client = Anthropic(api_key=api_key.strip())
                                    except ImportError:
                                        self.console.print("[yellow]Warning: anthropic package not installed. Install with: pip install anthropic[/yellow]")
                                
                                self.chat_service.config.set_model(model_name)
                                self.console.print(f"[success]Model set to: {model_name}[/success]")
                            else:
                                self.console.print("[yellow]Model selection canceled.[/yellow]")
                        
                        elif provider == "openai":
                            self.console.print("[yellow]This model requires an OpenAI API key.[/yellow]")
                            api_key = await self.session.prompt_async("Enter your OpenAI API key (or press Enter to cancel): ")
                            
                            if api_key.strip():
                                self.chat_service.config.OPENAI_API_KEY = api_key.strip()
                                self.chat_service.config._save_config()
                                
                                self.chat_service.openai_client = openai.OpenAI(api_key=api_key.strip())
                                
                                self.chat_service.config.set_model(model_name)
                                self.console.print(f"[success]Model set to: {model_name}[/success]")
                            else:
                                self.console.print("[yellow]Model selection canceled.[/yellow]")
                        
                        else:
                            self.console.print(f"[error]Unknown model provider: {provider}[/error]")
                    else:
                        self.chat_service.config.set_model(model_name)
                        self.console.print(f"[success]Model set to: {model_name}[/success]")
                else:
                    self.console.print("[error]Please enter a valid model number.[/error]")
            except ValueError:
                self.console.print("[error]Please enter a valid model number.[/error]")

    async def display_prompt_menu(self):
        """Display an interactive menu for prompt customization."""
        templates = self.chat_service.config.PROMPT_TEMPLATES
        current = self.chat_service.config.SYSTEM_PROMPT
        
        self.console.print("\n[bold]Prompt Customization[/bold]")
        self.console.print("Current prompt: \"{}\"".format(current[:50] + "..." if len(current) > 50 else current))
        self.console.print("\nAvailable templates:")
        
        template_list = list(templates.items())
        for i, (name, template) in enumerate(template_list, 1):
            indicator = "* " if template == current else "  "
            self.console.print(f"{i}. {indicator}{name}: \"{template[:40]}{'...' if len(template) > 40 else ''}\"")
        
        self.console.print("\n[bold]Options:[/bold]")
        self.console.print("1-{} - Use template".format(len(templates)))
        self.console.print("c - Create custom prompt")
        self.console.print("s - Save current prompt as template")
        self.console.print("r - Remove a template")
        self.console.print("q - Return to chat")
        
        choice = await self.session.prompt_async("Enter choice: ")
        
        if choice.lower() == 'c':
            self.console.print("Enter your custom prompt (press Enter twice to finish):")
            lines = []
            while True:
                line = await self.session.prompt_async("")
                if not line and lines:
                    break
                lines.append(line)
            
            if lines:
                new_prompt = "\n".join(lines)
                self.chat_service.config.update_system_prompt(new_prompt)
                self.console.print("[success]System prompt updated.[/success]")
        
        elif choice.lower() == 's':
            template_name = await self.session.prompt_async("Enter template name: ")
            if template_name.strip():
                self.chat_service.config.add_prompt_template(template_name.strip(), current)
                self.console.print(f"[success]Current prompt saved as template: {template_name}[/success]")
        
        elif choice.lower() == 'r':
            del_template = await self.session.prompt_async("Enter template number to remove: ")
            try:
                idx = int(del_template) - 1
                if 0 <= idx < len(template_list):
                    template_name, _ = template_list[idx]
                    if template_name != "default":
                        if self.chat_service.config.remove_prompt_template(template_name):
                            self.console.print(f"[success]Removed template: {template_name}[/success]")
                    else:
                        self.console.print("[error]Cannot remove the default template.[/error]")
            except ValueError:
                self.console.print("[error]Please enter a valid template number.[/error]")
        
        elif choice.isdigit():
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(template_list):
                    name, _ = template_list[idx]
                    self.chat_service.config.use_prompt_template(name)
                    self.console.print(f"[success]Now using prompt template: {name}[/success]")
            except ValueError:
                self.console.print("[error]Please enter a valid template number.[/error]")

    async def display_api_key_menu(self):
        self.console.print("\n[bold]API Key Management[/bold]")
        self.console.print("API keys are stored securely in your system's keychain.")
        self.console.print("\n[bold]Options:[/bold]")
        self.console.print("1 - Set OpenAI API key")
        self.console.print("2 - Set Tavily API key")
        self.console.print("3 - Set Exa API key")
        self.console.print("4 - Set Anthropic API key")
        self.console.print("q - Return to model menu")
        
        choice = await self.session.prompt_async("Enter choice: ")
        
        key_mapping = {
            "1": "OPENAI_API_KEY",
            "2": "TAVILY_API_KEY",
            "3": "EXA_API_KEY",
            "4": "ANTHROPIC_API_KEY"
        }
        
        if choice in key_mapping:
            key_name = key_mapping[choice]
            key_display = key_name.replace("_API_KEY", "")
            
            self.console.print(f"\n[bold]Setting {key_display} API Key[/bold]")
            self.console.print("[yellow]API keys are stored securely in your system's keychain.[/yellow]")
            
            new_key = getpass.getpass(f"Enter your {key_display} API key (input will be hidden): ")
            
            if new_key.strip():
                setattr(self.chat_service.config, key_name, new_key.strip())
                self.console.print(f"[success]{key_display} API key updated successfully[/success]")
                self.console.print(f"[info]First 4 characters: {new_key[:4]}{'*' * 20}[/info]")
            else:
                self.console.print("[yellow]No key provided. Operation canceled.[/yellow]")
        
        await self.display_model_menu()

    async def confirm_clear_all(self) -> bool:
        """Confirm if the user wants to clear all session data."""
        prompt_text = HTML("<prompt>Are you sure you want to clear all session data? Type \"yes\" to confirm: </prompt>")
        
        answer = await self.session.prompt_async(prompt_text, style=self.prompt_style)
        return answer.lower() == "yes"
    
    def display_help(self):
        help_text = """
        ===== Geegle Help =====
        - Ask any question to get an answer with web sources
        
        Basic Commands:
        - /clear - Clear current conversation history
        - /clear all - Clear all session data (requires confirmation)
        - /export [filename] - Export all sessions to a JSON file
        - /help - Show this help message
        - /rerank [on|off] - Enable or disable search result reranking
        
        Advanced Features:
        - /session [name] - Manage sessions or switch to named session
        - /model [name] - Change AI model or switch to named model
        - /prompt [text|name] - Change prompt or use named template
        
        Keyboard Shortcuts:
        - Tab - Autocomplete commands and arguments
        - ↑/↓ - Navigate command history
        
        - Type exit to quit the application
        """
        self.console.print(Panel(help_text, title="Geegle Help", expand=False))