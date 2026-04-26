"""
CS108 — End Semester Examination
Operation: VISION OS  —  SOLUTION

Bug fixes:
  Bug 1 (mkdir): used self.current_dir instead of _get_parent_path(path)
  Bug 2 (cd):    double slash when current_dir=='/' — added guard
  Bug 3 (read):  no type guard — added 'and entry["type"]=="file"'
  Bug 4 (ls):    missing sorted() — wrapped with sorted()
  Bug 5 (grep):  split() on whitespace — changed to split('\\n')
"""

import copy
import re


# =============================================================================
# PART 1 — FileSystem (bugs fixed)
# =============================================================================

class FileSystem:

    def __init__(self):
        self.root = {
            'type': 'directory',
            'name': '/',
            'children': {
                'home': {
                    'type': 'directory',
                    'name': 'home',
                    'children': {
                        'sushant': {
                            'type': 'directory',
                            'name': 'sushant',
                            'children': {
                                'nova_log.txt': {
                                    'type': 'file',
                                    'name': 'nova_log.txt',
                                    'content': 'NOVA was meant to save the world. She still can.'
                                }
                            }
                        }
                    }
                }
            }
        }
        self.current_dir = '/home/sushant'

    def pwd(self):
        return self.current_dir

    def _get_node(self, path):
        if path == '/':
            return self.root
        current = self.root
        for part in path.strip('/').split('/'):
            if part == '':
                continue
            if current['type'] != 'directory':
                return None
            if part not in current['children']:
                return None
            current = current['children'][part]
        return current

    def _get_parent_path(self, path):
        if path == '/':
            return '/'
        parent = path.rstrip('/').rsplit('/', 1)[0]
        return parent if parent != '' else '/'

    def mkdir(self, path):
        # FIX 1: navigate to parent of path, not current_dir
        parent_node = self._get_node(self._get_parent_path(path))
        dir_name    = path.rstrip('/').rsplit('/', 1)[-1]
        parent_node['children'][dir_name] = {
            'type': 'directory', 'name': dir_name, 'children': {}
        }

    def cd(self, path):
        if path == '..':
            self.current_dir = self._get_parent_path(self.current_dir)
        elif path.startswith('/'):
            self.current_dir = path.rstrip('/') or '/'
        else:
            # FIX 2: avoid double slash when already at '/'
            self.current_dir = ('/' + path
                                if self.current_dir == '/'
                                else self.current_dir + '/' + path)

    def touch(self, filename):
        node = self._get_node(self.current_dir)
        node['children'][filename] = {
            'type': 'file', 'name': filename, 'content': ''
        }

    def write(self, filename, content):
        node = self._get_node(self.current_dir)
        if filename in node['children']:
            node['children'][filename]['content'] = content
        else:
            node['children'][filename] = {
                'type': 'file', 'name': filename, 'content': content
            }

    def read(self, filename):
        node  = self._get_node(self.current_dir)
        entry = node['children'].get(filename)
        # FIX 3: guard against reading a directory node
        return entry['content'] if entry and entry['type'] == 'file' else ''

    def ls(self):
        # FIX 4: return sorted list
        return sorted(self._get_node(self.current_dir)['children'].keys())

    def grep(self, pattern, text):
        # FIX 5: split on newlines, not all whitespace
        lines = text.split('\n')
        return '\n'.join(line for line in lines if pattern in line)


# =============================================================================
# PART 2 — VersionControl
# =============================================================================

class VersionControl:

    def __init__(self, fs):
        self.fs             = fs
        self.commits        = {}
        self.branches       = {'main': None}
        self.head           = 'main'
        self.staging        = []
        self.commit_counter = 0

    def add(self, filepath):
        self.staging.append(filepath)

    def commit(self, message):
        self.commit_counter += 1
        self.commits[self.commit_counter] = {
            'message':     message,
            'staged':      list(self.staging),
            'root':        copy.deepcopy(self.fs.root),
            'current_dir': self.fs.current_dir
        }
        self.branches[self.head] = self.commit_counter
        self.staging             = []
        return self.commit_counter

    def branch(self, name):
        self.branches[name] = self.branches[self.head]

    def checkout(self, name):
        snap                = self.commits[self.branches[name]]
        self.fs.root        = copy.deepcopy(snap['root'])
        self.fs.current_dir = snap['current_dir']
        self.head           = name

    def status(self):
        return {'staged': list(self.staging), 'modified': []}


# =============================================================================
# PART 3 — NexusShell
# =============================================================================

class NexusShell:

    def __init__(self):
        self.fs = FileSystem()
        self.vc = VersionControl(self.fs)

    def run(self, command_string):
        command_string = command_string.strip()
        if not command_string:
            return None

        # Handle output redirection (>) — must check before pipe to avoid
        # treating '>' inside a piped command as redirection
        output_file = None
        if '>' in command_string and '|' not in command_string:
            left, right  = command_string.split('>', 1)
            command_string = left.strip()
            output_file    = right.strip()

        # Handle pipes
        if '|' in command_string:
            result = self._handle_pipe(command_string)
        else:
            result = self._execute(command_string)

        # Redirect output to file if '>' was present
        if output_file is not None and result is not None:
            self.fs.touch(output_file)
            self.fs.write(output_file, result)
            return None

        return result

    def _handle_pipe(self, command_string):
        parts  = command_string.split('|')
        output = None
        for part in parts:
            output = self._execute(part.strip(), piped=output)
        return output

    def _execute(self, command, piped=None):
        parts = command.strip().split()
        if not parts:
            return None
        cmd = parts[0]

        if cmd == 'pwd':
            return self.fs.pwd()

        elif cmd == 'ls':
            items = self.fs.ls()
            return '\n'.join(items) if items else ''

        elif cmd == 'mkdir':
            self.fs.mkdir(parts[1])
            return None

        elif cmd == 'cd':
            self.fs.cd(parts[1])
            return None

        elif cmd == 'touch':
            self.fs.touch(parts[1])
            return None

        elif cmd == 'echo':
            return ' '.join(parts[1:])

        elif cmd == 'cat':
            return self.fs.read(parts[1])

        elif cmd == 'grep':
            pattern = parts[1]
            # input comes from pipe; if no pipe, try second arg
            text = piped if piped is not None else (' '.join(parts[2:]) if len(parts) > 2 else '')
            return self.fs.grep(pattern, text)

        elif cmd == 'git':
            if len(parts) < 2:
                return None
            sub = parts[1]
            if sub == 'add':
                self.vc.add(parts[2])
                return None
            elif sub == 'commit':
                msg = command.split('"')[1] if '"' in command else parts[2]
                return f"Committed as ID {self.vc.commit(msg)}"
            elif sub == 'branch':
                self.vc.branch(parts[2])
                return None
            elif sub == 'checkout':
                self.vc.checkout(parts[2])
                return None
            elif sub == 'status':
                return f"Staged: {self.vc.status()['staged']}"

        elif cmd == 'help':
            return HELP_TEXT

        return f"Unknown command: {cmd}"


# =============================================================================
# HELP TEXT
# =============================================================================

HELP_TEXT = """
VISION OS  —  Commands
---------------------------------------------------------
  pwd / ls / mkdir / cd / touch
  echo <text>
  echo <text> > <file>
  cat <file>
  cat <file> | grep <pattern>
  git add / commit / branch / checkout / status
  help / exit
---------------------------------------------------------
"""


# =============================================================================
# INTERACTIVE SHELL
# =============================================================================

def main():
    shell = NexusShell()

    print("=" * 58)
    print("  VISION OS v1.0  —  Implant active.")
    print("  Sushant wrote it. Ansh held the door. Shanmathi set the clock.")
    print("  She left Python alive. That was her mistake.")
    print("=" * 58)
    print()

    while True:
        try:
            user_input = input(f"[VISION-OS {shell.fs.pwd()}]$ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDisconnecting.")
            break
        if not user_input:
            continue
        if user_input.lower() == 'exit':
            print("Disconnecting.")
            break
        try:
            result = shell.run(user_input)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == '__main__':
    main()
