#!/usr/bin/env python3
"""
File System Emulator - CLI Interface
Demonstrates three directory structure modes: Single-Level, Two-Level, Hierarchical
"""
import sys
from src.filesystem import FileSystemManager, FSMode


class CLI:
    """Command Line Interface for File System Emulator"""
    
    def __init__(self):
        self.fs = FileSystemManager()
        self.running = True
    
    def get_prompt(self) -> str:
        """Get the CLI prompt string"""
        mode_name = self.fs.mode.upper()
        path = self.fs.get_current_path()
        return f"[{mode_name}] {path}$ "
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"ERROR: {message}")
    
    def print_success(self, message: str):
        """Print success message"""
        print(message)
    
    def print_table(self, headers: list, rows: list):
        """Print a formatted table"""
        # Calculate column widths
        col_widths = []
        for i, header in enumerate(headers):
            max_width = len(header)
            for row in rows:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            col_widths.append(max_width + 2)
        
        # Print header
        header_line = ""
        for i, header in enumerate(headers):
            header_line += header.ljust(col_widths[i])
        print(header_line)
        print("-" * len(header_line))
        
        # Print rows
        for row in rows:
            row_line = ""
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    row_line += str(cell).ljust(col_widths[i])
            print(row_line)
    
    def execute_command(self, command: str):
        """Execute a CLI command"""
        parts = command.strip().split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        # Mode switching
        if cmd == "mode":
            if len(args) != 1:
                self.print_error("Usage: mode <single|two-level|hierarchical>")
                return
            success, message = self.fs.set_mode(args[0])
            if success:
                self.print_success(message)
            else:
                self.print_error(message)
            return
        
        # Help
        if cmd == "help" or cmd == "?":
            self.show_help()
            return
        
        # Exit
        if cmd == "exit" or cmd == "quit":
            self.running = False
            return
        
        # Reset
        if cmd == "reset":
            self.fs._reset_filesystem()
            self.print_success("File system reset to initial state")
            return
        
        # Create file
        if cmd == "create":
            if len(args) < 1:
                self.print_error("Usage: create <filename>")
                return
            success, message = self.fs.create_file(args[0])
            if success:
                self.print_success(message)
            else:
                self.print_error(message)
            return
        
        # Create directory
        if cmd == "mkdir":
            if len(args) < 1:
                self.print_error("Usage: mkdir <dirname>")
                return
            success, message = self.fs.create_directory(args[0])
            if success:
                self.print_success(message)
            else:
                self.print_error(message)
            return
        
        # Delete
        if cmd == "delete" or cmd == "rm":
            if len(args) < 1:
                self.print_error("Usage: delete <name> [--recursive]")
                return
            recursive = "--recursive" in args or "-r" in args
            name = args[0]
            success, message = self.fs.delete(name, recursive)
            if success:
                self.print_success(message)
            else:
                self.print_error(message)
            return
            
        # Rename
        if cmd == "rename":
            if len(args) < 2:
                self.print_error("Usage: rename <old_name> <new_name>")
                return
            success, message = self.fs.rename(args[0], args[1])
            if success:
                self.print_success(message)
            else:
                self.print_error(message)
            return
            
        # Info
        if cmd == "info" or cmd == "stat":
            if len(args) < 1:
                self.print_error("Usage: info <name>")
                return
            success, info, message = self.fs.get_info(args[0])
            if success:
                for k, v in info.items():
                    print(f"{k.ljust(12)}: {v}")
            else:
                self.print_error(message)
            return
        
        # Change directory
        if cmd == "cd":
            if len(args) < 1:
                self.print_error("Usage: cd <path>")
                return
            success, message = self.fs.change_directory(args[0])
            if not success:
                self.print_error(message)
            return
        
        # Print working directory
        if cmd == "pwd":
            print(self.fs.get_current_path())
            return
        
        # List contents
        if cmd == "ls" or cmd == "list":
            contents = self.fs.list_contents()
            if not contents:
                print("(empty directory)")
                return
            
            headers = ["Name", "Type", "Size", "Created"]
            rows = [[c['name'], c['type'], c['size'], c['created']] for c in contents]
            self.print_table(headers, rows)
            return
        
        # Tree view
        if cmd == "tree":
            print(self.fs.get_full_tree())
            return
        
        # Search
        if cmd == "search":
            if len(args) < 1:
                self.print_error("Usage: search <query>")
                return
            results = self.fs.search(args[0])
            if not results:
                print(f"No results found for '{args[0]}'")
                return
            
            print(f"Found {len(results)} result(s) for '{args[0]}':")
            for result in results:
                print(f"  {result['path']} ({result['type']}, {result['size']})")
            return
        
        # Show logs
        if cmd == "logs":
            logs = self.fs.get_logs()
            if not logs:
                print("No operations logged yet")
                return
            print("Operation Logs:")
            for log in logs:
                print(f"  {log}")
            return
        
        # Demo mode
        if cmd == "demo":
            self.run_demo()
            return
        
        # Unknown command
        self.print_error(f"Unknown command: '{cmd}'. Type 'help' for available commands")
    
    def show_help(self):
        """Display help information"""
        help_text = """
╔════════════════════════════════════════════════════════════════╗
║           File System Emulator - Help                          ║
╚════════════════════════════════════════════════════════════════╝

MODE SWITCHING:
  mode <single|two-level|hierarchical>  Switch directory structure mode

FILE OPERATIONS:
  create <filename>                    Create a new file
  mkdir <dirname>                      Create a new directory
  delete <name> [--recursive]          Delete file or directory
  rm <name> [--recursive]              Alias for delete
  rename <old> <new>                   Rename a file or folder
  info <name>                          Show file/folder details

NAVIGATION (Two-Level & Hierarchical only):
  cd <path>                            Change directory
  pwd                                  Print working directory

VIEWING:
  ls / list                            List directory contents
  tree                                 Show ASCII tree structure
  search <query>                       Search for files/directories

SYSTEM:
  reset                                Reset file system
  logs                                 Show operation logs
  demo                                 Run demonstration script
  help / ?                             Show this help
  exit / quit                          Exit the emulator

EXAMPLES:
  mode hierarchical
  mkdir home && cd home
  mkdir user1 && cd user1
  create file.txt
  tree
  search "*.txt"
"""
        print(help_text)
    
    def run_demo(self):
        """Run a demonstration script"""
        print("\n" + "="*60)
        print("RUNNING DEMONSTRATION")
        print("="*60 + "\n")
        
        print("1️⃣ Visual Directory Tree")
        
        # Phase 1: Single-Level
        print("\n🔹 Single-Level Directory")
        self.fs.set_mode(FSMode.SINGLE_LEVEL)
        self.fs.create_file("file1.txt")
        self.fs.create_file("file2.doc")
        self.fs.create_file("image.png")
        print("\nExample Output:\n")
        print(self.fs.get_full_tree())
        print("\nAll files are stored in one directory. No subfolders.\n")
        
        # Phase 2: Two-Level
        print("🔹 Two-Level Directory")
        self.fs.set_mode(FSMode.TWO_LEVEL)
        self.fs.create_directory("UserA")
        self.fs.change_directory("UserA")
        self.fs.create_file("notes.txt")
        self.fs.create_file("photo.jpg")
        self.fs.change_directory("..")
        self.fs.create_directory("UserB")
        self.fs.change_directory("UserB")
        self.fs.create_file("project.docx")
        self.fs.change_directory("..")
        print("\nExample Output:\n")
        print(self.fs.get_full_tree())
        print("\nEach user has a separate folder.\n")
        
        # Phase 3: Hierarchical
        print("🔹 Hierarchical (Tree-Based) Directory")
        self.fs.set_mode(FSMode.HIERARCHICAL)
        self.fs.create_directory("Documents")
        self.fs.change_directory("Documents")
        self.fs.create_directory("College")
        self.fs.change_directory("College")
        self.fs.create_file("assignment.pdf", size=int(2.4 * 1024 * 1024))
        self.fs.change_directory("..")
        self.fs.create_file("Resume.docx")
        self.fs.change_directory("..")
        self.fs.create_directory("Pictures")
        self.fs.change_directory("Pictures")
        self.fs.create_file("trip.png")
        self.fs.change_directory("..")
        self.fs.create_directory("Music")
        self.fs.change_directory("Music")
        self.fs.create_file("song.mp3")
        self.fs.change_directory("..")
        print("\nExample Output:\n")
        print(self.fs.get_full_tree())
        print("\nThis supports multiple levels of folders inside folders.\n")

        print("2️⃣ File Metadata Display")
        print("Example Output:\n")
        self.fs.change_directory("Documents/College")
        success, info, msg = self.fs.get_info("assignment.pdf")
        if success:
            for k, v in info.items():
                print(f"{k.ljust(12)}: {v}")
        
        print("\n\n3️⃣ Logs of Operations")
        print("Example Output:\n")
        self.fs._reset_filesystem()
        self.fs.create_directory("Documents")
        self.fs.change_directory("Documents")
        self.fs.create_file("assignment.pdf")
        self.fs.rename("assignment.pdf", "final_assignment.pdf")
        self.fs.delete("final_assignment.pdf")
        self.fs.change_directory("..")
        self.fs.create_directory("Pictures")
        self.fs.change_directory("Pictures")
        self.fs.create_file("trip.png")
        self.fs.change_directory("..")
        self.fs.search("trip.png")
        
        logs = self.fs.get_logs()
        for log in logs:
            print(log)
            
        print("\n" + "="*60)
        print("DEMONSTRATION COMPLETE")
        print("="*60 + "\n")
    
    def run(self):
        """Main CLI loop"""
        print("\n" + "="*60)
        print("  File System Emulator")
        print("  Demonstrating OS Directory Structures")
        print("="*60)
        print("\nType 'help' for commands or 'demo' to see a demonstration")
        print()
        
        while self.running:
            try:
                command = input(self.get_prompt())
                self.execute_command(command)
            except KeyboardInterrupt:
                print("\n\nUse 'exit' to quit")
            except EOFError:
                self.running = False
        
        print("\nGoodbye!")


def main():
    """Entry point"""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
