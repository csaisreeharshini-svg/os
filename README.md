# File System Emulator

An educational tool that demonstrates how Operating Systems manage file systems internally. This emulator showcases three distinct directory architecture paradigms with full CRUD operations, metadata management, and visual tree representation.

## Features

### Three Directory Structure Modes

1. **Single-Level Directory**
   - All files exist at root level only
   - No subdirectories allowed
   - Simulates early MS-DOS floppy disk systems

2. **Two-Level Directory**
   - Root contains only user directories
   - Files can only exist inside user folders
   - Maximum depth of 2 levels
   - Users are isolated from each other

3. **Hierarchical (Tree-Based) Directory**
   - Unlimited nesting depth (configurable, default 10)
   - Full parent-child relationships
   - Supports relative and absolute paths (.., ., /)
   - Modern file system structure

### Core Operations

- **File Operations**: `create`, `delete`, `ls` (list)
- **Directory Operations**: `mkdir`, `cd`, `pwd`
- **Visualization**: `tree` (ASCII art representation)
- **Search**: `search` with wildcard support (*, ?)
- **Mode Switching**: `mode` command to switch between structures

### Metadata Management

- File size (human-readable: B, KB, MB)
- Creation and modification timestamps
- File type detection
- Absolute path resolution

## Installation

No external dependencies required - uses Python 3.8+ standard library.

```bash
# Clone or download the project
cd os

# Run the emulator
python main.py
```

## Usage

### Basic Commands

```bash
# Switch to a directory structure mode
mode single
mode two-level
mode hierarchical

# Create files and directories
create file.txt
mkdir foldername

# Navigate (Two-Level & Hierarchical only)
cd foldername
cd ..
cd /absolute/path
pwd

# View contents
ls
tree

# Search
search "*.txt"
search "report"

# Delete
delete filename
delete foldername --recursive

# System commands
reset        # Reset file system
logs         # Show operation logs
help         # Show help
exit         # Exit
```

### Demo Mode

Run the built-in demonstration to see all three modes in action:

```bash
demo
```

## Example Session

```
[HIERARCHICAL] /$ mode hierarchical
Switched to HIERARCHICAL Directory - Root cleared

[HIERARCHICAL] /$ mkdir home
Created directory 'home'

[HIERARCHICAL] /$ cd home

[HIERARCHICAL] /home$ mkdir user1
Created directory 'user1'

[HIERARCHICAL] /home$ cd user1

[HIERARCHICAL] /home/user1$ create document.txt
Created file 'document.txt' (45.2KB)

[HIERARCHICAL] /home/user1$ tree
/
├── home/
│   └── user1/
│       └── document.txt [45.2KB | 14:30]

[HIERARCHICAL] /home/user1$ search "*.txt"
Found 1 result(s) for '*.txt':
  /home/user1/document.txt (File, 45.2KB)
```

## Project Structure

```
os/
├── main.py              # CLI entry point
├── src/
│   ├── __init__.py      # Package initialization
│   ├── models.py        # Node classes (BaseNode, FileNode, DirectoryNode)
│   └── filesystem.py    # FileSystemManager with mode support
├── plan.md              # Project specification
└── README.md            # This file
```

## OS Concepts Demonstrated

1. **Data Structures**: Tree-based directory structure using HashMap/Dict for O(1) lookup
2. **File Allocation**: Simulated file storage with metadata
3. **Path Resolution**: Absolute and relative path handling
4. **Directory Traversal**: Recursive algorithms for search and tree visualization
5. **Mode Constraints**: Enforcing structural rules based on OS architecture

## Complexity Analysis

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Create    | O(1)           | O(1)             |
| Delete    | O(1)           | O(1)             |
| Search    | O(n)           | O(n)             |
| Tree      | O(n)           | O(n)             |
| cd        | O(d)           | O(1)             |

Where n = total nodes, d = depth of path

## License

Educational project for OS concepts demonstration.
