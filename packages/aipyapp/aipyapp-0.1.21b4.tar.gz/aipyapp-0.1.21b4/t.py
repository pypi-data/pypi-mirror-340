from rich import print
from rich.panel import Panel
from rich.console import Console
import sys

DISCLAIMER_TEXT = """[bold yellow]⚠️  风险提示与免责声明 ⚠️[/bold yellow]

本程序可生成并执行由大型语言模型（LLM）自动生成的代码。请您在继续使用前，务必阅读并理解以下内容：

[bold]1. 风险提示：[/bold]
- 自动生成的代码可能包含逻辑错误、性能问题或不安全操作（如删除文件、访问网络、执行系统命令等）。
- 本程序无法保证生成代码的准确性、完整性或适用性。
- 在未充分审查的情况下运行生成代码，可能会对您的系统、数据或隐私造成损害。

[bold]2. 免责声明：[/bold]
- 本程序仅作为开发与测试用途提供，不对由其生成或执行的任何代码行为承担责任。
- 使用本程序即表示您理解并接受所有潜在风险，并同意对因使用本程序产生的任何后果自行负责。
"""

def show_disclaimer():
    console = Console()
    panel = Panel.fit(DISCLAIMER_TEXT, title="[bold red]免责声明", border_style="red", padding=(1, 2))
    console.print(panel)

    while True:
        console.print("\n[bold]是否确认已阅读并接受以上免责声明？（yes/no）：[/bold]", end=" ")
        response = input().strip().lower()
        if response in ("yes", "y"):
            console.print("[green]感谢确认，程序继续运行。[/green]")
            break
        elif response in ("no", "n"):
            console.print("[red]您未接受免责声明，程序将退出。[/red]")
            sys.exit(1)
        else:
            console.print("[yellow]请输入 yes 或 no。[/yellow]")

if __name__ == "__main__":
    show_disclaimer()
    # 你的主程序逻辑
    print("[cyan]程序正在运行...[/cyan]")
