"""
File System Manager with support for three directory structure modes
"""
import random
from typing import List, Optional, Tuple
from datetime import datetime
from .models import BaseNode, FileNode, DirectoryNode, NodeType


class FSMode:
    SINGLE_LEVEL = "single"
    TWO_LEVEL = "two-level"
    HIERARCHICAL = "hierarchical"


class FileSystemManager:
    """Manages the file system with different directory structure modes"""
    
    def __init__(self):
        self.root = DirectoryNode("")
        self.current_directory = self.root
        self.mode = FSMode.HIERARCHICAL
        self.max_depth = 10
        self.operation_log = []
    
    def set_mode(self, mode: str) -> Tuple[bool, str]:
        """Switch to a different directory structure mode"""
        if mode not in [FSMode.SINGLE_LEVEL, FSMode.TWO_LEVEL, FSMode.HIERARCHICAL]:
            return False, f"Invalid mode. Use: {FSMode.SINGLE_LEVEL}, {FSMode.TWO_LEVEL}, or {FSMode.HIERARCHICAL}"
        
        self.mode = mode
        self._reset_filesystem()
        return True, f"Switched to {mode.upper()} Directory - Root cleared"
    
    def _reset_filesystem(self):
        """Reset the file system to initial state"""
        self.root = DirectoryNode("")
        self.current_directory = self.root
        self.operation_log = []
    
    def _log_operation(self, message: str):
        """Log an operation"""
        timestamp = datetime.now().strftime("%I:%M %p")
        log_entry = f"[{timestamp}] {message}"
        self.operation_log.append(log_entry)
    
    def _validate_name(self, name: str) -> Tuple[bool, str]:
        """Validate file/directory name"""
        if not name:
            return False, "Name cannot be empty"
        
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            if char in name:
                return False, f"Invalid character '{char}' in name"
        
        if len(name) > 255:
            return False, "Name exceeds maximum length of 255 characters"
        
        return True, ""
    
    def create_file(self, name: str, size: Optional[int] = None) -> Tuple[bool, str]:
        """Create a new file in the current directory"""
        valid, error = self._validate_name(name)
        if not valid:
            return False, error
        
        if self.current_directory.has_child(name):
            return False, f"File '{name}' already exists"
        
        # Random size if not provided (1-100 KB)
        if size is None:
            size = random.randint(1, 100) * 1024
        
        file_node = FileNode(name, self.current_directory, size)
        success = self.current_directory.add_child(file_node)
        
        if success:
            dir_name = self.current_directory.name if self.current_directory.name else "Root"
            self._log_operation(f"File '{name}' created in {dir_name}")
            return True, f"Created file '{name}' ({file_node.format_size()})"
        
        return False, f"Failed to create file '{name}'"
    
    def create_directory(self, name: str) -> Tuple[bool, str]:
        """Create a new directory in the current directory"""
        valid, error = self._validate_name(name)
        if not valid:
            return False, error
        
        # Mode-specific validation
        if self.mode == FSMode.SINGLE_LEVEL:
            return False, "Error: Subdirectories not allowed in Single-Level structure"
        
        if self.mode == FSMode.TWO_LEVEL:
            current_depth = self.current_directory.get_depth()
            if current_depth >= 1:
                return False, "Error: Maximum depth (2 levels) exceeded in Two-Level structure"
        
        if self.mode == FSMode.HIERARCHICAL:
            current_depth = self.current_directory.get_depth()
            if current_depth >= self.max_depth:
                return False, f"Error: Maximum depth ({self.max_depth} levels) exceeded"
        
        if self.current_directory.has_child(name):
            return False, f"Directory '{name}' already exists"
        
        dir_node = DirectoryNode(name, self.current_directory)
        success = self.current_directory.add_child(dir_node)
        
        if success:
            self._log_operation(f"Folder '{name}' created")
            return True, f"Created directory '{name}'"
        
        return False, f"Failed to create directory '{name}'"
    
    def delete(self, name: str, recursive: bool = False) -> Tuple[bool, str]:
        """Delete a file or directory"""
        node = self.current_directory.get_child(name)
        
        if node is None:
            return False, f"'{name}' not found"
        
        if isinstance(node, DirectoryNode) and not node.is_empty() and not recursive:
            return False, f"Directory '{name}' is not empty. Use 'delete {name} --recursive'"
        
        success = self.current_directory.remove_child(name)
        
        if success:
            node_type = 'Folder' if isinstance(node, DirectoryNode) else 'File'
            self._log_operation(f"{node_type} '{name}' deleted")
            return True, f"Deleted '{name}'"
        
        return False, f"Failed to delete '{name}'"
    
    def rename(self, old_name: str, new_name: str) -> Tuple[bool, str]:
        """Rename a file or directory"""
        valid, error = self._validate_name(new_name)
        if not valid:
            return False, error
            
        node = self.current_directory.get_child(old_name)
        if node is None:
            return False, f"'{old_name}' not found"
            
        if self.current_directory.has_child(new_name):
            return False, f"'{new_name}' already exists"
            
        self.current_directory.remove_child(old_name)
        node.name = new_name
        if isinstance(node, FileNode):
            node.extension = new_name.split('.')[-1] if '.' in new_name else ""
        self.current_directory.add_child(node)
        
        node_type = 'Folder' if isinstance(node, DirectoryNode) else 'File'
        self._log_operation(f"{node_type} '{old_name}' renamed to '{new_name}'")
        return True, f"Renamed '{old_name}' to '{new_name}'"

    def get_info(self, name: str) -> Tuple[bool, dict, str]:
        """Get file/directory metadata"""
        node = self.current_directory.get_child(name)
        if node is None:
            return False, {}, f"'{name}' not found"
        
        info = {
            'File Name': node.name,
            'File Size': node.format_size(),
            'File Type': node.get_file_type() if isinstance(node, FileNode) else 'Directory',
            'Access Mode': node.access_mode,
            'Created On': node.created_at.strftime("%d-%m-%Y %I:%M %p"),
        }
        return True, info, ""

    def change_directory(self, path: str) -> Tuple[bool, str]:
        """Change current directory (cd command)"""
        if self.mode == FSMode.SINGLE_LEVEL:
            return False, "Directory navigation not available in Single-Level mode"
        
        if path == "..":
            if self.current_directory.parent is None:
                return False, "Already at root directory"
            self.current_directory = self.current_directory.parent
            return True, ""
        
        if path == "." or path == "":
            return True, ""
        
        if path.startswith("/"):
            # Absolute path
            target = self.root
            parts = [p for p in path.split("/") if p]
        else:
            # Relative path
            target = self.current_directory
            parts = [p for p in path.split("/") if p]
        
        for part in parts:
            if part == "..":
                if target.parent is not None:
                    target = target.parent
            elif part == ".":
                continue
            else:
                child = target.get_child(part)
                if child is None:
                    return False, f"Path not found: '{part}'"
                if not isinstance(child, DirectoryNode):
                    return False, f"'{part}' is not a directory"
                target = child
        
        self.current_directory = target
        return True, ""
    
    def get_current_path(self) -> str:
        """Get the current working directory path"""
        return self.current_directory.get_path()
    
    def list_contents(self) -> List[dict]:
        """List contents of current directory"""
        contents = []
        for name, node in self.current_directory.children.items():
            contents.append({
                'name': name,
                'type': 'Dir' if isinstance(node, DirectoryNode) else 'File',
                'size': node.format_size(),
                'created': node.created_at.strftime("%b %d, %H:%M")
            })
        return sorted(contents, key=lambda x: (x['type'] == 'File', x['name']))
    
    def search(self, query: str) -> List[dict]:
        """Search for files/directories recursively"""
        results = []
        self._search_recursive(self.current_directory, query, results)
        
        if results:
            first_path = results[0]['path']
            parts = first_path.split('/')
            found_in = parts[-2] if len(parts) > 1 and parts[-2] else "Root"
            self._log_operation(f"Search performed for '{query}' – Found in {found_in}")
        else:
            self._log_operation(f"Search performed for '{query}' – No results found")
            
        return results
    
    def _search_recursive(self, directory: DirectoryNode, query: str, results: List[dict]):
        """Helper method for recursive search"""
        for name, node in directory.children.items():
            # Check if name matches query (supports wildcards)
            if self._matches_pattern(name, query):
                results.append({
                    'name': name,
                    'path': node.get_path(),
                    'type': 'Dir' if isinstance(node, DirectoryNode) else 'File',
                    'size': node.format_size()
                })
            
            # Recursively search in subdirectories
            if isinstance(node, DirectoryNode):
                self._search_recursive(node, query, results)
    
    def _matches_pattern(self, name: str, pattern: str) -> bool:
        """Check if name matches pattern (supports * and ? wildcards)"""
        import re
        # Convert wildcard pattern to regex
        regex_pattern = pattern.replace('.', r'\.')
        regex_pattern = regex_pattern.replace('*', '.*')
        regex_pattern = regex_pattern.replace('?', '.')
        regex_pattern = f"^{regex_pattern}$"
        return re.match(regex_pattern, name, re.IGNORECASE) is not None
    
    def get_tree(self) -> str:
        """Get ASCII tree representation of current directory"""
        return self._build_tree(self.current_directory, "", True)
    
    def _build_tree(self, directory: DirectoryNode, prefix: str, is_last: bool) -> str:
        """Build ASCII tree recursively"""
        result = ""
        children = list(directory.children.values())
        
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            connector = " └── " if is_last_child else " ├── "
            
            if isinstance(child, DirectoryNode):
                result += f"{prefix}{connector}{child.name}/\n"
                new_prefix = prefix + ("     " if is_last_child else " │   ")
                result += self._build_tree(child, new_prefix, is_last_child)
            else:
                result += f"{prefix}{connector}{child.name}\n"
        
        return result
    
    def get_full_tree(self) -> str:
        """Get ASCII tree from root"""
        return f"Root/\n{self._build_tree(self.root, '', True)}".rstrip()
    
    def get_logs(self) -> List[str]:
        """Get operation logs"""
        return self.operation_log
