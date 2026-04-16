"""
CS108 — End Semester Examination
Operation: VISION OS — Implant the Shell. Save the Nexus.

*** SOLUTION FILE — NOT FOR DISTRIBUTION ***

Student Name:   [SOLUTION]
Roll Number:    [SOLUTION]
"""

import copy
import re


# =============================================================================
# PART 1: FileSystem Class
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
                        'tony': {
                            'type': 'directory',
                            'name': 'tony',
                            'children': {
                                'mission.txt': {
                                    'type': 'file',
                                    'name': 'mission.txt',
                                    'content': 'Implant the shell. Save the Nexus.'
                                }
                            }
                        }
                    }
                }
            }
        }
        self.current_dir = '/home/tony'

    def pwd(self):
        return self.current_dir

    def _get_node(self, path):
        if path == '/':
            return self.root
        parts = path.strip('/').split('/')
        current = self.root
        for part in parts:
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

    # ── Student implementations ───────────────────────────────────────────────

    def mkdir(self, path):
        parent_path = self._get_parent_path(path)
        parent_node = self._get_node(parent_path)
        dir_name    = path.rstrip('/').rsplit('/', 1)[-1]
        parent_node['children'][dir_name] = {
            'type':     'directory',
            'name':     dir_name,
            'children': {}
        }

    def cd(self, path):
        if path == '..':
            self.current_dir = self._get_parent_path(self.current_dir)
        elif path.startswith('/'):
            self.current_dir = path.rstrip('/') or '/'
        else:
            if self.current_dir == '/':
                self.current_dir = '/' + path
            else:
                self.current_dir = self.current_dir + '/' + path

    def touch(self, filename):
        node = self._get_node(self.current_dir)
        node['children'][filename] = {
            'type':    'file',
            'name':    filename,
            'content': ''
        }

    def write(self, filename, content):
        node = self._get_node(self.current_dir)
        if filename in node['children']:
            node['children'][filename]['content'] = content
        else:
            node['children'][filename] = {
                'type':    'file',
                'name':    filename,
                'content': content
            }

    def read(self, filename):
        node = self._get_node(self.current_dir)
        entry = node['children'].get(filename)
        if entry and entry['type'] == 'file':
            return entry['content']
        return ''

    def ls(self):
        node = self._get_node(self.current_dir)
        return sorted(node['children'].keys())

    def grep(self, pattern, text):
        lines = text.split('\n')
        return '\n'.join(line for line in lines if pattern in line)


# =============================================================================
# PART 2: VersionControl Class
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
        self.staging = []
        return self.commit_counter

    def branch(self, name):
        self.branches[name] = self.branches[self.head]

    def checkout(self, name):
        snapshot             = self.commits[self.branches[name]]
        self.fs.root         = copy.deepcopy(snapshot['root'])
        self.fs.current_dir  = snapshot['current_dir']
        self.head            = name

    def status(self):
        return {'staged': list(self.staging), 'modified': []}


# =============================================================================
# PART 3: NexusShell Class
# =============================================================================

class NexusShell:

    def __init__(self):
        self.fs = FileSystem()
        self.vc = VersionControl(self.fs)

    def run(self, command_string):
        command_string = command_string.strip()
        if not command_string:
            return None
        if '|' in command_string:
            return self._handle_pipe(command_string)
        return self._execute_single(command_string)

    def _handle_pipe(self, command_string):
        output = None
        for part in command_string.split('|'):
            output = self._execute_single(part.strip(), input_text=output)
        return output

    def _execute_single(self, command, input_text=None):
        parts = command.strip().split()
        if not parts:
            return None
        cmd = parts[0]

        if cmd == 'pwd':
            return self.fs.pwd()

        elif cmd == 'ls':
            entries = self.fs.ls()
            return '\n'.join(entries) if entries else ''

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
            if '>' in command:
                left, right = command.split('>', 1)
                text     = left.replace('echo', '', 1).strip()
                filename = right.strip()
                self.fs.touch(filename)
                self.fs.write(filename, text)
            return None

        elif cmd == 'cat':
            return self.fs.read(parts[1])

        elif cmd == 'grep':
            return self.fs.grep(parts[1], input_text or '')

        elif cmd == 'git':
            if len(parts) < 2:
                return None
            sub = parts[1]

            if sub == 'add':
                self.vc.add(parts[2])
                return None

            elif sub == 'commit':
                message = command.split('"')[1] if '"' in command else parts[2]
                cid     = self.vc.commit(message)
                return f"Committed as ID {cid}"

            elif sub == 'branch':
                self.vc.branch(parts[2])
                return None

            elif sub == 'checkout':
                self.vc.checkout(parts[2])
                return None

            elif sub == 'status':
                s = self.vc.status()
                return f"Staged: {s['staged']}"

        elif cmd == 'help':
            return HELP_TEXT

        return f"Unknown command: {cmd}"


# =============================================================================
# HELP TEXT
# =============================================================================

HELP_TEXT = """
VISION OS  —  Available Commands
---------------------------------------------------------
  pwd                      Print current directory
  ls                       List files and folders
  mkdir <path>             Make a new directory
  cd <path>                Change directory  (supports ..)
  touch <file>             Create an empty file
  echo <text> > <file>     Write text to a file
  cat <file>               Read a file
  cat <file> | grep <word> Filter lines containing word

  git add <path>           Stage a file
  git commit "<message>"   Save a snapshot
  git branch <n>        Create a branch
  git checkout <n>      Switch to a branch
  git status               Show staged files

  help                     Show this message
  exit                     Shut down VISION OS
---------------------------------------------------------
"""


# =============================================================================
# INTERACTIVE SHELL
# =============================================================================

def main():
    shell = NexusShell()

    print("=" * 60)
    print("  VISION OS v1.0  —  Implant active.")
    print("  Running inside Ultron's network.")
    print("  He left Python alive. That was his mistake.")
    print("  Type 'help' for commands. Type 'exit' to disconnect.")
    print("=" * 60)
    print()

    while True:
        cwd    = shell.fs.pwd()
        prompt = f"[VISION-OS {cwd}]$ "
        try:
            user_input = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDisconnecting. The implant remains.")
            break
        if not user_input:
            continue
        if user_input.lower() == 'exit':
            print("Disconnecting. The implant remains.")
            break
        try:
            result = shell.run(user_input)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"[ERROL] {e}")


if __name__ == '__main__':
    main()
