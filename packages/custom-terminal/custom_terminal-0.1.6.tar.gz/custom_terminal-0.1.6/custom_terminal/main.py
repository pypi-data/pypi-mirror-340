import os
import cmd
from pathlib import Path
from dotenv import load_dotenv

try:
    # Try relative import first (works in installed package)
    from .commands.base_commands import BaseCommands
    from .commands.weather import WeatherCommand
except ImportError:
    # Fallback to absolute import (works in development)
    from commands.base_commands import BaseCommands
    from commands.weather import WeatherCommand

class CustomTerminal(cmd.Cmd):
    prompt = 'user@custom-terminal:~$ '
    
    def __init__(self):
        super().__init__()
        # Load .env from package directory if exists
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        
        self.base_commands = BaseCommands()
        self.weather_command = WeatherCommand()
    
    def default(self, line):
        if line.lower() == 'exit':
            return True
        
        # Try base commands first
        base_result = self.base_commands.execute(line)
        if base_result is not None:
            print(base_result)
            return False
        
        # Try weather command
        weather_result = self.weather_command.execute(line)
        if weather_result is not None:
            print(weather_result)
            return False
        
        print(f"Command not found: {line}")

def main():
    print("Welcome to Custom Terminal! Type 'help' for available commands.")
    CustomTerminal().cmdloop()

if __name__ == "__main__":
    main()