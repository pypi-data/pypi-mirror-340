import os
import subprocess

class BaseCommands:
    def execute(self, command):
        cmd_parts = command.split()
        if not cmd_parts:
            return None
        
        # Implement basic Linux commands
        if cmd_parts[0] == 'ls':
            return '\n'.join(os.listdir(cmd_parts[1] if len(cmd_parts) > 1 else '.'))
        elif cmd_parts[0] == 'pwd':
            return os.getcwd()
        elif cmd_parts[0] == 'echo':
            return ' '.join(cmd_parts[1:])
        elif cmd_parts[0] in ['cd', 'mkdir', 'rm', 'cat']:
            try:
                subprocess.run(command, shell=True, check=True)
                return ""
            except subprocess.CalledProcessError as e:
                return f"Error: {e}"
        
        return None