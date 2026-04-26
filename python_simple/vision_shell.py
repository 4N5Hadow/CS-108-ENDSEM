"""
CS108 — End Semester Examination
Operation: VISION OS

Student Name:   [YOUR NAME HERE]
Roll Number:    [YOUR ROLL NUMBER HERE]

Run inside NOVA_shell:
    NOVA@NEXUS ~> python3 vision_shell.py

Allowed imports: copy, re  (nothing else)
No real file I/O. All data lives in RAM.
"""

import copy
import re


# =============================================================================
# PART 1 — FileSystem  [5 marks]
#
# Sushant designed this class. Shanmathi implemented it under fire.
# She flagged bugs before she could fix them. Find them. Fix them.
#
# There are at least 5 bugs in this implementation.
# 4 marks for the 4 public assertions below. 1 mark for a hidden test.
#
# Public assertions (all must pass after your fixes):
#
#   fs = FileSystem()
#   fs.cd('/')
#   fs.mkdir('/ops')
#   fs.cd('ops')
#   assert fs.pwd() == '/ops'                             # (a)
#
#   fs2 = FileSystem()
#   fs2.cd('/')
#   assert fs2.read('home') == ''                         # (b)
#
#   fs3 = FileSystem()
#   fs3.touch('zebra.txt')
#   fs3.touch('alpha.txt')
#   assert fs3.ls()[-1] == 'zebra.txt'                    # (c)
#
#   fs4 = FileSystem()
#   log = 'resistance is live\nNOVA wins\nresistance fights back'
#   assert fs4.grep('resistance', log) == \
#          'resistance is live\nresistance fights back'   # (d)
#
# Every bug is a single-line change.
# The score command runs only public tests. Write your own edge cases.
# Even the public tests may change for final scoring.
# =============================================================================

class FileSystem:

    # ── GIVEN — do not change __init__ or the two helpers ────────────────────

    def __init__(self):
        """Boot with Sushant's directory pre-created."""
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

    # ── FIX THE BUGS BELOW ────────────────────────────────────────────────────

    def mkdir(self, path):
        parent_node = self._get_node(self.current_dir)        # <- bug?
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
            self.current_dir = self.current_dir + '/' + path  # <- bug?

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
        return entry['content'] if entry else ''               # <- bug?

    def ls(self):
        return list(self._get_node(self.current_dir)['children'].keys())  # <- bug?

    def grep(self, pattern, text):
        lines = text.split()                                   # <- bug?
        return '\n'.join(line for line in lines if pattern in line)


# =============================================================================
# PART 2 — VersionControl  [5 marks]
# =============================================================================

class VersionControl:
    """
    Snapshot-based version control.
    commit() must deep-copy the entire filesystem tree.
    """

    def __init__(self, fs):
        self.fs             = fs
        self.commits        = {}
        self.branches       = {'main': None}
        self.head           = 'main'
        self.staging        = []
        self.commit_counter = 0

    def add(self, filepath):
        """Append filepath to staging list."""
        # TODO
        pass

    def commit(self, message):
        """
        Snapshot the entire FS. Return commit ID (int, starts at 1).
        Clear staging after committing.
        """
        # TODO
        pass

    def branch(self, name):
        """Create branch pointing to current commit."""
        # TODO
        pass

    def checkout(self, name):
        """
        Switch to branch. Restore FS tree and current_dir from
        that branch's snapshot (deep-copy on restore).
        """
        # TODO
        pass

    def status(self):
        """Return {'staged': [...], 'modified': []}."""
        # TODO
        pass


# =============================================================================
# PART 3 — NexusShell  [5 marks]
#
# Implement NexusShell from scratch.
# Provide a run(command_string) method that handles:
#   - Output redirection:  echo hi > file.txt
#   - Pipes:               cat file.txt | grep hi
#   - All commands in the table below
#
# The main() loop at the bottom shows how run() is called.
# =============================================================================

class NexusShell:
    """
    Commands to support:
        pwd
        ls
        mkdir <path>
        cd <path>
        touch <file>
        echo <text>                 returns the text
        cat <file>                  returns file contents
        grep <pattern>              filters piped input
        git add <path>
        git commit "<msg>"          returns "Committed as ID N"
        git branch <name>
        git checkout <name>
        git status                  returns "Staged: [...]"
        help

    Shell-level handling:
        <cmd> > <file>   redirect output to file (write, not append)
        <cmd1> | <cmd2>  pipe output of cmd1 as input to cmd2
    """

    def __init__(self):
        self.fs = FileSystem()
        self.vc = VersionControl(self.fs)

    def run(self, command_string):
        # TODO: implement
        pass


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
# INTERACTIVE SHELL  —  do not change
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
