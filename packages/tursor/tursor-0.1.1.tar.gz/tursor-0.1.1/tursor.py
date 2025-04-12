import click
import os
import requests
from dotenv import load_dotenv

load_dotenv()
server_url = os.getenv('SERVER_URL')

def colored_text(text, color):
    """Return colored text"""
    return click.style(text, fg=color)

# make this goood
def gather_context(error_outputs):
    """Relevant file paths from error output"""
    print(error_outputs)
    context = {}
    import re
    file_paths = re.findall(r'([a-zA-Z0-9_\-\/\.]+\.(dart|py|js|ts))', error_outputs)
    for path, _ in file_paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                context[path] = content
    return context


def execute_command(command):
    """Execute a command"""
    try:
        import subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': str(e),
            'returncode': 1
        }

@click.group()
def cli():
    """tursor: The AI Code Terminal"""
    pass

@cli.command()
@click.argument('command', nargs=-1, required=True)
def fix(command):
    """Fix errors in command execution"""
    cmd_str = ' '.join(command)
    click.echo(f"Running: {cmd_str}")

    result = execute_command(cmd_str)
    
    if result['returncode'] == 0:
        click.echo(result['stdout'])
        click.echo(colored_text("Command executed successfully", 'green'))
        return
    
    click.echo(colored_text("Error detected", "red"))
    error_output = result['stderr'] or result['stdout']

    context = gather_context(error_output)
    try:
        print("Sending request to server...", server_url )
        response = requests.post(
            f'{server_url}/api/fix',
            json={
                'command': cmd_str,
                'error_output': error_output,
                'code_context': context
            }
        )
        print(response)
    except requests.exceptions.RequestException as e:
        click.echo(colored_text(f"Server down, please contact krishavrajsingh@gmail.com ASAP!!", "red"))
        return

if __name__ == "__main__":
    cli()