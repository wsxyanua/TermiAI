import os
import subprocess
from typing import Optional, List, Dict
import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from rich.spinner import Spinner
import json
from pathlib import Path
import ollama
from datetime import datetime
import time
from ollama import Client
from rich.table import Table
from rich.align import Align

# Initialize Typer app and Rich console
app = typer.Typer()
console = Console()

# Constants
HISTORY_FILE = os.path.expanduser("~/.ai_terminal_history.json")
SCRIPTS_DIR = os.path.expanduser("~/.ai_terminal_scripts")
AVAILABLE_MODELS = {
    "deepseek-coder": "deepseek-coder",
    "deepseek-r1": "deepseek-r1"
}
DEFAULT_MODEL = "deepseek-coder"

def load_history() -> list:
    """Load command history from file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history: list):
    """Save command history to file."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def get_ai_suggestion(user_input: str, history: List[Dict[str, str]], model: str, mode: str = "command") -> str:
    """Get AI suggestion based on user input and mode."""
    try:
        # Construct prompt based on mode
        if mode == "command":
            prompt = f"Convert this request to a shell command: {user_input}"
        elif mode == "explain":
            prompt = f"Explain this shell command: {user_input}"
        elif mode == "fix":
            prompt = f"Fix this incorrect shell command: {user_input}"
        elif mode == "chat":
            prompt = f"Answer this technical question: {user_input}"
        elif mode == "search":
            prompt = f"Convert this search request to a find command: {user_input}"
        else:
            prompt = user_input

        # Add history context if available
        if history:
            history_context = "\n".join([f"Request: {h['request']}\nCommand: {h['command']}" for h in history[-5:]])
            prompt = f"Previous commands:\n{history_context}\n\nNew request: {prompt}"

        # Show loading spinner
        with console.status("[bold green]Đang xử lý...[/bold green]"):
            # Get response from Ollama
            client = Client()
            response = client.generate(model=model, prompt=prompt)
            # Extract the response text from the dictionary
            return response.get('response', 'Không nhận được phản hồi từ AI')

    except Exception as e:
        console.print(f"[red]Error getting AI suggestion: {str(e)}[/red]")
        return None

def execute_command(command: str) -> tuple[bool, str]:
    """Execute a shell command and return success status and output."""
    try:
        result = os.popen(command).read()
        return True, result
    except Exception as e:
        return False, str(e)

def save_script(history: list, description: str = ""):
    """Save current session commands as a shell script."""
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{SCRIPTS_DIR}/script_{timestamp}.sh"
    
    with open(filename, 'w') as f:
        f.write("#!/bin/bash\n\n")
        if description:
            f.write(f"# {description}\n")
        f.write(f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for entry in history:
            f.write(f"# {entry['request']}\n")
            f.write(f"{entry['command']}\n\n")
    
    os.chmod(filename, 0o755)
    return filename

@app.command()
def main(model: str = DEFAULT_MODEL):
    """AI Terminal Assistant main function."""
    if model not in AVAILABLE_MODELS:
        console.print(Panel(f"[red]Lỗi: Model {model} không khả dụng.\nCác model hỗ trợ: {', '.join(AVAILABLE_MODELS.keys())}[/red]", title="[bold red]Lỗi Model[/bold red]", border_style="red"))
        return

    # Load history
    history = load_history()
    
    # Welcome message
    welcome_panel = Panel(
        Align.center(
            f"""
[bold cyan]AI Terminal Assistant[/bold cyan] [bold magenta]bởi:[/bold magenta] [white]xyanua.[/white]
[green]Trợ lý AI giúp bạn làm việc với terminal hiệu quả hơn[/green]
[bold yellow]Model:[/bold yellow] [white]{model}[/white]

[dim]Gõ lệnh tự nhiên hoặc 'help' để xem hướng dẫn[/dim]
            """,
            vertical="middle"
        ),
        title="[bold blue]Chào mừng[/bold blue]",
        border_style="bright_magenta",
        padding=(1, 4),
    )
    console.print(welcome_panel)
    
    while True:
        try:
            # Stylish prompt
            user_input = Prompt.ask("[bold green]Bạn muốn làm gì?[/bold green]", default="help")
            
            # Đổi model động
            if user_input.lower().startswith('model '):
                new_model = user_input[6:].strip()
                if new_model in AVAILABLE_MODELS:
                    model = new_model
                    console.print(Panel(f"[green]Đã chuyển sang model:[/green] [bold]{model}[/bold]", border_style="green"))
                else:
                    console.print(Panel(f"[red]Model '{new_model}' không khả dụng.\nCác model hỗ trợ: {', '.join(AVAILABLE_MODELS.keys())}[/red]", border_style="red"))
                continue
            
            # Handle special commands
            if user_input.lower() == 'exit':
                console.print(Panel("[bold yellow]Tạm biệt! Hẹn gặp lại.[/bold yellow]", border_style="yellow"))
                break
            elif user_input.lower() == 'help':
                help_panel = Panel(
                    Align.left(
                        """
[bold]Các lệnh đặc biệt:[/bold]
- help: Hiển thị hướng dẫn
- exit: Thoát chương trình
- history: Xem lịch sử lệnh
- model: Xem thông tin mô hình hoặc đổi model (model <tên_model>)
- save: Lưu phiên làm việc thành script

[bold]Chế độ thông minh:[/bold]
- explain <lệnh>: Giải thích lệnh
- fix <lệnh>: Sửa lệnh sai
- chat <câu hỏi>: Hỏi đáp kỹ thuật
- search <mô tả>: Tìm kiếm file
                        """
                    ),
                    title="[bold cyan]Hướng dẫn sử dụng[/bold cyan]",
                    border_style="cyan",
                    padding=(1, 2)
                )
                console.print(help_panel)
                continue
            elif user_input.lower() == 'history':
                if not history:
                    console.print(Panel("[yellow]Chưa có lịch sử lệnh nào.[/yellow]", border_style="yellow"))
                else:
                    table = Table(title="[bold green]Lịch sử lệnh[/bold green]", show_lines=True, header_style="bold magenta")
                    table.add_column("#", style="dim", width=4)
                    table.add_column("Yêu cầu", style="cyan")
                    table.add_column("Lệnh", style="green")
                    table.add_column("Thời gian", style="yellow")
                    for idx, entry in enumerate(history[-10:], 1):
                        table.add_row(str(idx), entry['request'], entry['command'], entry.get('timestamp', '-'))
                    console.print(table)
                continue
            elif user_input.lower() == 'model':
                model_panel = Panel(
                    f"[bold]Model hiện tại:[/bold] [green]{model}[/green]\n[bold]Các model khả dụng:[/bold] [cyan]{', '.join(AVAILABLE_MODELS.keys())}[/cyan]",
                    title="[bold blue]Thông tin mô hình[/bold blue]",
                    border_style="blue"
                )
                console.print(model_panel)
                continue
            elif user_input.lower() == 'save':
                description = Prompt.ask("[bold yellow]Nhập mô tả cho script (tùy chọn)[/bold yellow]", default="")
                filename = save_script(history, description)
                console.print(Panel(f"[green]Script đã lưu tại:[/green] [bold]{filename}[/bold]", border_style="green"))
                continue
            
            # Determine mode
            mode = "command"
            if user_input.lower().startswith("explain "):
                mode = "explain"
                user_input = user_input[8:]
            elif user_input.lower().startswith("fix "):
                mode = "fix"
                user_input = user_input[4:]
            elif user_input.lower().startswith("chat "):
                mode = "chat"
                user_input = user_input[5:]
            elif user_input.lower().startswith("search "):
                mode = "search"
                user_input = user_input[7:]
            
            # Get AI suggestion with loading spinner
            response = get_ai_suggestion(user_input, history, model, mode)
            if not response:
                continue
            
            # Handle response based on mode
            if mode == "command":
                command_panel = Panel(
                    f"[bold green]Lệnh gợi ý:[/bold green]\n[white]{response}[/white]",
                    title="[bold green]Gợi ý lệnh[/bold green]",
                    border_style="green"
                )
                console.print(command_panel)
                if Prompt.ask("[bold yellow]Bạn có muốn thực thi lệnh này không?[/bold yellow]", choices=["y", "n"], default="n") == "y":
                    success, output = execute_command(response)
                    if success:
                        console.print(Panel("[green]Lệnh đã thực thi thành công![/green]", border_style="green"))
                        console.print(Panel(output, border_style="bright_black", title="[bold]Kết quả[/bold]"))
                        history.append({
                            "request": user_input,
                            "command": response,
                            "timestamp": datetime.now().isoformat()
                        })
                        save_history(history)
                    else:
                        console.print(Panel(f"[red]Lỗi khi thực thi lệnh:[/red]\n{output}", border_style="red"))
            else:
                result_panel = Panel(
                    response,
                    title="[bold magenta]Kết quả[/bold magenta]",
                    border_style="magenta"
                )
                console.print(result_panel)
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Dùng 'exit' để thoát chương trình[/yellow]")
        except Exception as e:
            console.print(Panel(f"[red]Lỗi: {str(e)}[/red]", border_style="red"))

if __name__ == "__main__":
    app() 
