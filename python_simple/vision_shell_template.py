"""
CS108 — End Semester Examination
Operation: VISION OS — Implant the Shell. Save the Nexus.

Student Name:   [YOUR NAME HERE]
Roll Number:    [YOUR ROLL NUMBER HERE]

HOW TO RUN:
    Inside ultron_shell:
        ULTRON@NEXUS ~> python3 vision_shell.py

RULES:
    - Allowed imports: copy, re  (nothing else)
    - No real file I/O  (no open, os, pathlib, subprocess, etc.)
    - All data must live in RAM — Python dictionaries and lists only
    - Do NOT change class names or method signatures
"""

import copy
import re


# =============================================================================
# PART 1: FileSystem Class  [5 marks]
# =============================================================================

class FileSystem:
    """
    An in-memory hierarchical filesystem stored as a tree of nested dicts.

    self.current_dir — string tracking current location, e.g. '/home/tony'

    Study __init__ carefully. It shows you exactly how the tree is structured.
    Every method you write must work with that same structure.
    """

    # ── GIVEN TO YOU — do not change ─────────────────────────────────────────

    def __init__(self):
        """
        Boot the filesystem. The Nexus starts with Tony's directory
        already in place, and drops you straight into it.
        """
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
        """Return current working directory path as a string."""
        return self.current_dir

    def _get_node(self, path):
        """
        Navigate the tree and return the node dict at the given absolute path.
        Returns None if the path does not exist.

        Use this in every method that needs to look up a directory or file.
        """
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
        """
        Return the parent directory path of the given absolute path.

        Examples:
            '/home/tony'  ->  '/home'
            '/home'       ->  '/'
            '/'           ->  '/'
        """
        if path == '/':
            return '/'
        parent = path.rstrip('/').rsplit('/', 1)[0]
        return parent if parent != '' else '/'

    # ── TODO: implement the methods below ────────────────────────────────────

    def mkdir(self, path):
        """
        Create a new directory at the given absolute path.
        The parent directory must already exist.

        Args:
            path (str): absolute path  e.g. '/home/tony/logs'

        Example:
            fs.mkdir('/home/tony/logs')
            fs.mkdir('/tmp')
        """
        # TODO
        pass

    def cd(self, path):
        """
        Change the current working directory. Does not return anything.

        Supports three forms:
            cd('/home/tony')   absolute path
            cd('logs')         relative — child of current directory
            cd('..')           go up one level

        Args:
            path (str): target directory
        """
        # TODO
        pass

    def touch(self, filename):
        """
        Create an empty file in the current directory.

        Args:
            filename (str): name only, not a path  e.g. 'notes.txt'

        Example:
            fs.touch('notes.txt')   # creates notes.txt with content = ''
        """
        # TODO
        pass

    def write(self, filename, content):
        """
        Write a string into a file in the current directory.

        Args:
            filename (str): name only
            content  (str): string to write

        Example:
            fs.write('notes.txt', 'Ultron last seen at sector 7')
        """
        # TODO
        pass

    def read(self, filename):
        """
        Read and return the content of a file in the current directory.
        Return '' if the file does not exist.

        Args:
            filename (str): name only

        Returns:
            str: file content, or '' if not found

        Example:
            fs.read('notes.txt')   # -> 'Ultron last seen at sector 7'
            fs.read('ghost.txt')   # -> ''
        """
        # TODO
        pass

    def ls(self):
        """
        Return a sorted list of all file and directory names in the
        current directory.

        Returns:
            list[str]: sorted names

        Example:
            fs.ls()   # -> ['logs', 'mission.txt', 'notes.txt']
        """
        # TODO
        pass

    def grep(self, pattern, text):
        """
        Filter a multi-line string, keeping only lines containing pattern.

        Args:
            pattern (str): search term
            text    (str): multi-line string (lines separated by '\\n')

        Returns:
            str: matching lines joined by '\\n'

        Example:
            fs.grep('Ultron', 'Ultron spotted\\nAll clear\\nUltron retreating')
            # -> 'Ultron spotted\\nUltron retreating'
        """
        # TODO
        pass


# =============================================================================
# PART 2: VersionControl Class  [5 marks]
# =============================================================================

class VersionControl:
    """
    Simplified in-memory version control.
    Stores deep-copy snapshots of the entire filesystem tree per commit.
    """

    # ── GIVEN TO YOU — do not change ─────────────────────────────────────────

    def __init__(self, fs):
        self.fs             = fs
        self.commits        = {}              # { commit_id : snapshot_dict }
        self.branches       = {'main': None}  # { branch_name : commit_id }
        self.head           = 'main'          # currently active branch
        self.staging        = []              # files staged for next commit
        self.commit_counter = 0

    # ── TODO: implement the methods below ────────────────────────────────────

    def add(self, filepath):
        """
        Stage a file path for the next commit.

        Args:
            filepath (str): e.g. '/home/tony/notes.txt'

        Example:
            vc.add('/home/tony/notes.txt')
        """
        # TODO
        pass

    def commit(self, message):
        """
        Save a snapshot of the entire filesystem state.
        Returns the commit ID (integer, starts at 1, increments by 1).
        Clears the staging list after committing.

        The snapshot must be a deep copy — see Module Reference for copy.deepcopy.

        Args:
            message (str): short description

        Returns:
            int: commit ID

        Example:
            vc.commit("Tony's plan saved")   # -> 1
        """
        # TODO
        pass

    def branch(self, name):
        """
        Create a new branch pointing to the current commit.

        Args:
            name (str): branch name  e.g. 'dev'

        Example:
            vc.branch('dev')
        """
        # TODO
        pass

    def checkout(self, name):
        """
        Switch to a branch and restore the filesystem to that branch's
        last committed snapshot (tree and current_dir both restored).
        Use deep copy when restoring so the stored snapshot stays intact.

        Args:
            name (str): branch name

        Example:
            vc.checkout('main')
        """
        # TODO
        pass

    def status(self):
        """
        Return current staging status.

        Returns:
            dict: {'staged': [list of staged paths], 'modified': []}

        Example:
            vc.add('/home/tony/notes.txt')
            vc.status()
            # -> {'staged': ['/home/tony/notes.txt'], 'modified': []}
        """
        # TODO
        pass


# =============================================================================
# PART 3: NexusShell Class  [5 marks]
# =============================================================================

class NexusShell:
    """
    Interactive shell tying FileSystem and VersionControl together.

    The interactive loop, prompt display, and pipe-splitting are already
    written. You implement _execute_single only.
    """

    # ── GIVEN TO YOU — do not change ─────────────────────────────────────────

    def __init__(self):
        self.fs = FileSystem()
        self.vc = VersionControl(self.fs)

    def run(self, command_string):
        """Execute one or more piped commands. Returns output or None."""
        command_string = command_string.strip()
        if not command_string:
            return None
        if '|' in command_string:
            return self._handle_pipe(command_string)
        return self._execute_single(command_string)

    def _handle_pipe(self, command_string):
        """Chain commands on | passing each output as the next input_text."""
        output = None
        for part in command_string.split('|'):
            output = self._execute_single(part.strip(), input_text=output)
        return output

    # ── TODO: implement _execute_single ──────────────────────────────────────

    def _execute_single(self, command, input_text=None):
        """
        Parse and execute a single command string.

        Args:
            command    (str):      the command to run
            input_text (str|None): piped text from previous command, or None

        Returns:
            str | None: output to display, or None for silent commands

        Commands to handle:

            pwd
            ls
            mkdir <path>
            cd <path>
            touch <filename>
            echo <text> > <filename>
            cat <filename>
            grep <pattern>            <- uses input_text when piped
            git add <filepath>
            git commit "<message>"    <- output: "Committed as ID N"
            git branch <name>
            git checkout <name>
            git status                <- output: "Staged: [...]"
            help
        """
        parts = command.strip().split()
        if not parts:
            return None

        cmd = parts[0]

        # TODO: implement all command cases
        pass


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
  git branch <name>        Create a branch
  git checkout <name>      Switch to a branch
  git status               Show staged files

  help                     Show this message
  exit                     Shut down VISION OS
---------------------------------------------------------
"""


# =============================================================================
# INTERACTIVE SHELL  —  GIVEN TO YOU, do not change
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
            print(f"[ERROR] {e}")


if __name__ == '__main__':
    main()
