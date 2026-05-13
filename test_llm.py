import pytest
import traceback
import time
from llm import call_chat_api, sanitize_messages

def test_sanitize_messages():
    raw_messages = [
        {"role": "user", "content": "Hello"}
    ]
    sanitized = sanitize_messages(raw_messages)
    assert len(sanitized) == 1, "Length of sanitized messages should be 1"
    assert sanitized[0]["role"] == "user", "Role should be user"
    assert sanitized[0]["content"] == "Hello", "Content should be Hello"

def test_call_chat_api():
    messages = [{"role": "user", "content": "Hello, this is a test. Just say 'OK'"}]
    response = call_chat_api(messages)
    
    # Validate that we got a valid response object
    assert response is not None, "API response was None"
    assert hasattr(response, "choices"), "Response object missing 'choices' attribute"
    assert len(response.choices) > 0, "Response choices list is empty"
    
    message = response.choices[0].message
    assert message is not None, "Message object is None"
    assert message.role == "assistant", f"Expected role 'assistant', got {message.role}"
    assert isinstance(message.content, str), "Message content is not a string"
    assert len(message.content) > 0, "Message content is empty"

if __name__ == "__main__":
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    console = Console()
    console.print()
    console.print(Panel("[bold blue]Starting LLM API Test Suite[/bold blue]", expand=False, border_style="blue"))
    
    tests = [
        ("test_sanitize_messages", test_sanitize_messages),
        ("test_call_chat_api", test_call_chat_api)
    ]
    
    table = Table(title="Test Execution Report", show_lines=True)
    table.add_column("Test Method", style="cyan", no_wrap=True)
    table.add_column("Status", style="bold")
    table.add_column("Duration", justify="right")
    table.add_column("Details / Failure Reason", style="dim")
    
    for name, test_func in tests:
        start_time = time.time()
        try:
            console.print(f"[dim]Running {name}...[/dim]")
            test_func()
            duration = time.time() - start_time
            table.add_row(name, "[green]PASSED ✓[/green]", f"{duration:.2f}s", "All assertions passed.")
        except AssertionError as e:
            duration = time.time() - start_time
            error_msg = str(e) or "AssertionError"
            table.add_row(name, "[red]FAILED ✗[/red]", f"{duration:.2f}s", f"[red]{error_msg}[/red]")
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"{e.__class__.__name__}: {str(e)}"
            table.add_row(name, "[red]ERROR ⚠[/red]", f"{duration:.2f}s", f"[red]{error_msg}[/red]")
            
    console.print()
    console.print(table)
    console.print()
