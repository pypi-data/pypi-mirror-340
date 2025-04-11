import json
import urllib.parse
import urllib.robotparser as robotparser
from typing import Dict, List, Any, Optional
import openai
from rich.console import Console
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from geegle.config import Config
from geegle.session_manager import SessionManager

class ChatService:    
    def __init__(self, session_manager: Optional[SessionManager] = None):
        self.config = Config.load()
        self.client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
        self.console = Console()
        
        self.session_manager = session_manager or SessionManager()
    
    @property
    def message_history(self) -> List[Dict[str, Any]]:
        return self.session_manager.get_session_history()
    
    async def search_tavily(self, query: str) -> Dict[str, Any]:
        url = "https://api.tavily.com/search"
        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.config.TAVILY_API_KEY}"
        }
        payload = {
            "query": query,
            "search_depth": "advanced",
            "include_domains": [],
            "exclude_domains": []
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.ConnectionError as e:
            return {"error": f"Connection error: {str(e)}"}
        except requests.Timeout as e:
            return {"error": f"Request timed out: {str(e)}"}
        except requests.HTTPError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"error": f"Error during search: {str(e)}"}
    
    async def search_exa(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Search academic papers using Exa API."""
        url = "https://api.exa.ai/search"
        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.config.EXA_API_KEY}"
        }
        payload = {
            "query": query,
            "numResults": max_results,
            "category": "research paper"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.ConnectionError as e:
            return {"error": f"Connection error: {str(e)}"}
        except requests.Timeout as e:
            return {"error": f"Request timed out: {str(e)}"}
        except requests.HTTPError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"error": f"Error during academic search: {str(e)}"}
    
    def check_robots_txt(self, url: str) -> bool:
        try:
            parsed_url = urllib.parse.urlparse(url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
            
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                parser = robotparser.RobotFileParser()
                parser.parse(response.text.splitlines())
                return parser.can_fetch("*", url)
            return True
        except Exception:
            return True 
    
    async def scrape_url(self, url: str) -> Dict[str, Any]:
        if not self.check_robots_txt(url):
            return {
                "error": "Scraping not allowed by robots.txt",
                "url": url
            }
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            try:
                driver.get(url)
                
                for selector in ['nav', 'header', 'footer', 'script', 'style', 'iframe']:
                    elements = driver.find_elements(By.TAG_NAME, selector)
                    for element in elements:
                        driver.execute_script("arguments[0].remove();", element)
                
                article = driver.find_elements(By.TAG_NAME, 'article')
                if article:
                    content_element = article[0]
                else:
                    content_element = driver.find_element(By.TAG_NAME, 'body')
                
                title = driver.title
                desc_elems = driver.find_elements(By.CSS_SELECTOR, 'meta[name="description"]')
                description = desc_elems[0].get_attribute('content') if desc_elems else None
                lang = driver.find_element(By.TAG_NAME, 'html').get_attribute('lang')
                
                return {
                    "title": title,
                    "content": content_element.text,
                    "url": url,
                    "metadata": {
                        "description": description,
                        "language": lang
                    }
                }
            except WebDriverException as e:
                return {
                    "error": f"Browser error: {str(e)}",
                    "url": url
                }
            finally:
                driver.quit()
        except WebDriverException as e:
            return {
                "error": f"WebDriver error: {str(e)}",
                "url": url
            }
        except Exception as e:
            return {
                "error": f"Unexpected error during scraping: {str(e)}",
                "url": url
            }
    
    def format_tavily_results(self, results: List[Dict[str, Any]]) -> str:
        formatted = []
        
        for i, result in enumerate(results[:5]):
            excerpt = result.get('snippet') or result.get('content', '')[:200]
            formatted.append(f"[{i + 1}] {result.get('title', 'No title')}\n{excerpt}\n")
        
        return "\n".join(formatted)
    
    async def chat(self, input_text: str):
        try:
            history = self.message_history
            tavily_results = []
            
            if input_text:
                self.console.print("[yellow]Searching for information...[/yellow]")
                search_response = await self.search_tavily(input_text)
                
                if "error" in search_response:
                    self.console.print(f"[red]Search error: {search_response['error']}[/red]")
                    self.console.print("[yellow]Proceeding without search results...[/yellow]")
                    user_message_content = f"Question: {input_text}"
                else:
                    tavily_results = search_response.get('results', [])
                    formatted_results = self.format_tavily_results(tavily_results)
                    
                    user_message_content = f"Based on the following web search results, please answer the question.\n\nSearch Results:\n{formatted_results}\n\nQuestion: {input_text}"
                
                history.append({"role": "user", "content": user_message_content})
                self.console.print(f"\nQuestion: {input_text}\n")
            
            self.console.print("[yellow]Generating answer...[/yellow]")
            self.console.print("[blue]\nAnswer:[/blue]")
            
            messages = [
                {
                    "role": "system", 
                    "content": "You are a helpful CLI assistant. When provided with web search results, use them to inform your answers."
                },
                *history
            ]
            
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "search",
                        "description": "Search the web for real-time information",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Search query"}
                            },
                            "required": ["query"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "academicSearch",
                        "description": "Search for academic papers and research",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Research query"},
                                "maxResults": {"type": "number", "description": "Maximum number of results", "default": 5}
                            },
                            "required": ["query"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "fetchWebContent",
                        "description": "Fetch and analyze content from a specific URL",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "url": {"type": "string", "description": "URL to fetch"}
                            },
                            "required": ["url"]
                        }
                    }
                }
            ]
            
            try:
                completion = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=messages,
                    tools=tools,
                    stream=True
                )
                
                assistant_message = {
                    "role": "assistant",
                    "content": ""
                }
                tool_calls = []
                current_tool_call = None
                
                for chunk in completion:
                    delta = chunk.choices[0].delta
                    
                    if delta.content:
                        assistant_message["content"] += delta.content
                        self.console.print(delta.content, end="")
                    
                    if delta.tool_calls:
                        for tool_call_delta in delta.tool_calls:
                            if tool_call_delta.index is not None and len(tool_calls) <= tool_call_delta.index:
                                current_tool_call = {
                                    "id": "",
                                    "type": "function",
                                    "function": {"name": "", "arguments": ""}
                                }
                                tool_calls.append(current_tool_call)
                            
                            if current_tool_call:
                                if tool_call_delta.id:
                                    current_tool_call["id"] += tool_call_delta.id
                                
                                if tool_call_delta.function and tool_call_delta.function.name:
                                    current_tool_call["function"]["name"] += tool_call_delta.function.name
                                
                                if tool_call_delta.function and tool_call_delta.function.arguments:
                                    current_tool_call["function"]["arguments"] += tool_call_delta.function.arguments
            except openai.APIError as e:
                self.console.print(f"[red]OpenAI API Error: {str(e)}[/red]")
                return
            except openai.APIConnectionError as e:
                self.console.print(f"[red]Connection Error: {str(e)}[/red]")
                return
            except openai.RateLimitError as e:
                self.console.print(f"[red]Rate Limit Error: {str(e)}[/red]")
                return
            except Exception as e:
                self.console.print(f"[red]Error generating response: {str(e)}[/red]")
                return
            
            self.console.print("\n")
            
            if tool_calls:
                assistant_message["tool_calls"] = tool_calls
            
            history.append(assistant_message)
            self.session_manager.update_session_history(history)
            
            if input_text and tavily_results:
                self.console.print("[yellow]\n===== SOURCES =====[/yellow]")
                for i, result in enumerate(tavily_results):
                    self.console.print(f"[cyan][{i + 1}] {result.get('title', 'Unknown title')}[/cyan]")
                    self.console.print(f"    {result.get('url', 'Unknown URL')}", style="dim")
                self.console.print("[yellow]==================\n[/yellow]")
            elif input_text:
                self.console.print("[red]No sources found for this query.[/red]")
            
            if tool_calls:
                additional_sources = []
                
                self.console.print("[yellow]\nGathering additional information...[/yellow]")
                
                for tool_call in tool_calls:
                    function_name = tool_call["function"]["name"]
                    tool_response = {"error": "Unknown function"}
                    
                    try:
                        args = json.loads(tool_call["function"]["arguments"])
                        
                        self.console.print(f"[yellow]Gathering data for {function_name}...[/yellow]")
                        
                        if function_name == "search":
                            tool_response = await self.search_tavily(args["query"])
                            if "results" in tool_response:
                                for result in tool_response["results"]:
                                    additional_sources.append({
                                        "title": result.get("title", "Unknown"),
                                        "url": result.get("url", "Unknown URL"),
                                        "type": "web"
                                    })
                        
                        elif function_name == "academicSearch":
                            tool_response = await self.search_exa(
                                args["query"], 
                                max_results=args.get("maxResults", 5)
                            )
                            if "results" in tool_response:
                                for result in tool_response["results"]:
                                    additional_sources.append({
                                        "title": result.get("title", "Unknown"),
                                        "url": result.get("url", "Unknown URL"),
                                        "type": "academic"
                                    })
                        
                        elif function_name == "fetchWebContent":
                            tool_response = await self.scrape_url(args["url"])
                            if "title" in tool_response:
                                additional_sources.append({
                                    "title": tool_response["title"],
                                    "url": args["url"],
                                    "type": "webpage"
                                })
                    except json.JSONDecodeError:
                        tool_response = {"error": "Invalid JSON in function arguments"}
                    except Exception as e:
                        tool_response = {"error": f"Error processing {function_name}: {str(e)}"}
                    
                    history.append({
                        "role": "tool",
                        "content": json.dumps(tool_response),
                        "tool_call_id": tool_call["id"]
                    })
                    
                    self.session_manager.update_session_history(history)
                    self.console.print("[green]✓ Done[/green]")
                
                if additional_sources:
                    self.console.print("\n[yellow]Additional Sources:[/yellow]")
                    for i, source in enumerate(additional_sources):
                        self.console.print(f"[cyan][{i + 1}] {source['title']}[/cyan]")
                        self.console.print(f"    {source['url']}", style="dim")
                    self.console.print("")
                
                self.console.print("[yellow]Generating final response...[/yellow]")
                await self.chat("")
        
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
    
    def get_history(self) -> List[Dict[str, Any]]:
        return self.message_history
    
    def clear_history(self):
        self.session_manager.update_session_history([])
    
    def get_current_session(self) -> str:
        return self.session_manager.get_current_session()
    
    def list_sessions(self) -> List[str]:
        return self.session_manager.list_sessions()
    
    async def switch_session(self, session_name: str) -> bool:
        return self.session_manager.switch_session(session_name)
    
    async def delete_session(self, session_name: str) -> bool:
        return self.session_manager.delete_session(session_name)