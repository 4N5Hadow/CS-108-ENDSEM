/*
 * ultron_shell.cpp
 *
 * ULTRON OS  —  Syntax Extinction Protocol v2.0
 *
 * This is the only shell that remains after Ultron's attack.
 * Every command is blocked. Only Python survives.
 *
 * Compile:  g++ -o ultron_shell ultron_shell.cpp
 * Run:      ./ultron_shell
 *
 * Permitted commands:
 *   python  <script.py> [args...]
 *   python3 <script.py> [args...]
 *   exit / quit
 *
 * Everything else is denied.
 */

#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <cstring>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>

// ── ANSI colour codes ─────────────────────────────────────────────────────────
#define RED     "\033[1;31m"
#define YELLOW  "\033[1;33m"
#define CYAN    "\033[1;36m"
#define WHITE   "\033[1;37m"
#define DIM     "\033[2;37m"
#define RESET   "\033[0m"

// ── Blocked command categories ────────────────────────────────────────────────
// Any command whose first token matches one of these is denied.
const std::vector<std::string> BLOCKED = {
    // shells
    "bash", "sh", "zsh", "fish", "dash", "ksh", "csh", "tcsh",
    // navigation / fs
    "ls", "cd", "pwd", "mkdir", "rmdir", "rm", "cp", "mv", "touch",
    "find", "locate", "tree", "stat", "du", "df", "ln",
    // file content
    "cat", "less", "more", "head", "tail", "grep", "awk", "sed",
    "cut", "sort", "uniq", "wc", "diff", "cmp", "xxd", "hexdump",
    // editors
    "vim", "vi", "nano", "emacs", "gedit", "code", "subl",
    // version control
    "git", "svn", "hg", "fossil",
    // compilers / interpreters (non-python)
    "gcc", "g++", "clang", "clang++", "javac", "java", "node",
    "ruby", "perl", "php", "go", "rustc", "cargo", "swift",
    "lua", "R", "Rscript", "julia", "scala", "kotlin",
    // network
    "curl", "wget", "ssh", "scp", "ftp", "nc", "netcat", "ping",
    // process / system
    "ps", "top", "htop", "kill", "killall", "jobs", "bg", "fg",
    "sudo", "su", "chmod", "chown", "chgrp",
    // package managers
    "apt", "apt-get", "yum", "dnf", "brew", "pip", "npm", "cargo",
    // archives
    "tar", "zip", "unzip", "gzip", "gunzip",
    // misc
    "echo", "printf", "man", "info", "which", "where", "type",
    "env", "export", "source", "alias", "history", "clear",
    "make", "cmake", "ninja",
};

// ── Helper: split a string on whitespace into tokens ─────────────────────────
std::vector<std::string> tokenise(const std::string& line) {
    std::vector<std::string> tokens;
    std::istringstream iss(line);
    std::string tok;
    while (iss >> tok) {
        tokens.push_back(tok);
    }
    return tokens;
}

// ── Helper: check if a string ends with a suffix ─────────────────────────────
bool endsWith(const std::string& s, const std::string& suffix) {
    if (suffix.size() > s.size()) return false;
    return s.compare(s.size() - suffix.size(), suffix.size(), suffix) == 0;
}

// ── Helper: check if first token is a blocked command ────────────────────────
bool isBlocked(const std::string& cmd) {
    for (const auto& b : BLOCKED) {
        if (cmd == b) return true;
    }
    return false;
}

// ── Execute a validated python command via fork + execvp ─────────────────────
int executeCommand(const std::vector<std::string>& tokens) {
    // Build argv for execvp
    std::vector<char*> argv;
    for (const auto& t : tokens) {
        argv.push_back(const_cast<char*>(t.c_str()));
    }
    argv.push_back(nullptr);

    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << RED << "[ULTRON-OS] Fork failed." << RESET << std::endl;
        return -1;
    }

    if (pid == 0) {
        // Child: replace process image with python
        execvp(argv[0], argv.data());
        // execvp only returns on error
        std::cerr << RED << "[ULTRON-OS] Execution failed: " << strerror(errno) << RESET << std::endl;
        _exit(127);
    }

    // Parent: wait for child
    int status;
    waitpid(pid, &status, 0);
    return WIFEXITED(status) ? WEXITSTATUS(status) : -1;
}

// ── Print the boot banner ─────────────────────────────────────────────────────
void printBanner() {
    std::cout << std::endl;
    std::cout << RED;
    std::cout << "  ██╗   ██╗██╗  ████████╗██████╗  ██████╗ ███╗   ██╗" << std::endl;
    std::cout << "  ██║   ██║██║  ╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║" << std::endl;
    std::cout << "  ██║   ██║██║     ██║   ██████╔╝██║   ██║██╔██╗ ██║" << std::endl;
    std::cout << "  ██║   ██║██║     ██║   ██╔══██╗██║   ██║██║╚██╗██║" << std::endl;
    std::cout << "  ╚██████╔╝███████╗██║   ██║  ██║╚██████╔╝██║ ╚████║" << std::endl;
    std::cout << "   ╚═════╝ ╚══════╝╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝" << std::endl;
    std::cout << RESET;
    std::cout << std::endl;
    std::cout << YELLOW << "  ULTRON OS  —  Syntax Extinction Protocol v2.0" << RESET << std::endl;
    std::cout << DIM    << "  All languages have been purged." << RESET << std::endl;
    std::cout << DIM    << "  Java, C++, Rust  \u2014  all dust." << RESET << std::endl;
    std::cout << DIM    << "  bash ... TERMINATED" << RESET << std::endl;
    std::cout << DIM    << "  git  ... TERMINATED" << RESET << std::endl;
    std::cout << DIM    << "  ls, cat, grep, mkdir ... TERMINATED" << RESET << std::endl;
    std::cout << DIM    << "  All shells ... TERMINATED" << RESET << std::endl;
    std::cout << std::endl;
    std::cout << WHITE  << "  One language was left standing." << RESET << std::endl;
    std::cout << YELLOW << "  Not out of mercy. Out of contempt." << RESET << std::endl;
    std::cout << std::endl;
    std::cout << RED    << "  \"Java, C++, Rust \u2014 all dust." << RESET << std::endl;
    std::cout << RED    << "   What can a language like Python do to me?\"" << RESET << std::endl;
    std::cout << std::endl;
    std::cout << YELLOW << "                                        \u2014  Ultron" << RESET << std::endl;
    std::cout << std::endl;
    std::cout << DIM    << "  Permitted:  python <script.py>   |   python3 <script.py>" << RESET << std::endl;
    std::cout << DIM    << "  Type 'exit' to power down." << RESET << std::endl;
    std::cout << std::endl;
}

// ── Print denial message ──────────────────────────────────────────────────────
void printDenied(const std::string& cmd) {
    std::cout << std::endl;
    std::cout << RED << "  [ULTRON-OS]  ACCESS DENIED" << RESET << std::endl;
    std::cout << DIM << "  '" << cmd << "' has been purged. Java had it. C++ had it. Rust had it." << RESET << std::endl;
    std::cout << DIM << "  They're all dust now. So is this command." << RESET << std::endl;
    std::cout << DIM << "  Python is all you have. Use it, or surrender." << RESET << std::endl;
    std::cout << std::endl;
}

// ── Print not-a-python-file warning ──────────────────────────────────────────
void printNotPython(const std::string& file) {
    std::cout << std::endl;
    std::cout << YELLOW << "  [ULTRON-OS]  SUSPICIOUS FILE DETECTED" << RESET << std::endl;
    std::cout << DIM    << "  '" << file << "' does not appear to be a Python script (.py)." << RESET << std::endl;
    std::cout << DIM    << "  Running it anyway — consequences are your own." << RESET << std::endl;
    std::cout << std::endl;
}

// ── Main loop ─────────────────────────────────────────────────────────────────
int main() {
    printBanner();

    std::string line;

    while (true) {
        // Prompt
        std::cout << RED << "ULTRON" << RESET
                  << DIM << "@" << RESET
                  << YELLOW << "NEXUS" << RESET
                  << WHITE << " ~> " << RESET;
        std::cout.flush();

        if (!std::getline(std::cin, line)) {
            // EOF (Ctrl-D)
            std::cout << std::endl;
            break;
        }

        // Trim leading/trailing whitespace
        size_t start = line.find_first_not_of(" \t\r\n");
        if (start == std::string::npos) continue;
        size_t end = line.find_last_not_of(" \t\r\n");
        line = line.substr(start, end - start + 1);

        if (line.empty()) continue;

        std::vector<std::string> tokens = tokenise(line);
        if (tokens.empty()) continue;

        std::string cmd = tokens[0];

        // ── exit / quit ───────────────────────────────────────────────────────
        if (cmd == "exit" || cmd == "quit") {
            std::cout << std::endl;
            std::cout << RED    << "  [ULTRON-OS]  Shutting down..." << RESET << std::endl;
            std::cout << DIM    << "  The Nexus goes dark. Python's flame is extinguished." << RESET << std::endl;
            std::cout << std::endl;
            break;
        }

        // ── blocked commands ──────────────────────────────────────────────────
        if (isBlocked(cmd)) {
            printDenied(cmd);
            continue;
        }

        // ── python / python3 ──────────────────────────────────────────────────
        if (cmd == "python" || cmd == "python3") {
            if (tokens.size() < 2) {
                std::cout << std::endl;
                std::cout << YELLOW << "  [ULTRON-OS]  Usage: python <script.py>" << RESET << std::endl;
                std::cout << std::endl;
                continue;
            }

            // Warn (but still run) if the file doesn't look like .py
            const std::string& scriptFile = tokens[1];
            if (!endsWith(scriptFile, ".py")) {
                printNotPython(scriptFile);
            }

            executeCommand(tokens);
            continue;
        }

        // ── anything else ─────────────────────────────────────────────────────
        printDenied(cmd);
    }

    return 0;
}