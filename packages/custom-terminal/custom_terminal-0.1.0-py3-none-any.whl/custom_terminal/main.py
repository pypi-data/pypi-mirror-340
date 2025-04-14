#!/usr/bin/env python3
import sys
import cmd
from custom_terminal.commands import base_commands, weather

class CustomTerminal(cmd.Cmd):
    prompt = 'user@custom-terminal:~$ '
    
    def __init__(self):
        super().__init__()
        self.base_commands = base_commands.BaseCommands()
        self.weather_command = weather.WeatherCommand()
    
    def default(self, line):
        if line.lower() == 'exit':
            return True
        
        # Check base commands first
        base_result = self.base_commands.execute(line)
        if base_result is not None:
            print(base_result)
            return False
        
        # Check weather command
        weather_result = self.weather_command.execute(line)
        if weather_result is not None:
            print(weather_result)
            return False
        
        print(f"Command not found: {line}")
    
    def do_help(self, arg):
        """Show available commands"""
        print("\nAvailable commands:")
        print("------------------")
        print("Standard Linux commands: ls, cd, pwd, mkdir, rm, cat, echo")
        print("Custom commands:")
        print("  weather <location> - Get weather for a specific location")
        print("  help - Show this help message")
        print("  exit - Quit the terminal")
        print()

def main():
    terminal = CustomTerminal()
    print("Welcome to Custom Terminal! Type 'help' for available commands.")
    terminal.cmdloop()

if __name__ == "__main__":
    main()