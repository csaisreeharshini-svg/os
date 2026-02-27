"""
Core Node classes for File System Emulator
"""
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class NodeType(Enum):
    FILE = "FILE"
    DIRECTORY = "DIRECTORY"


class BaseNode:
    """Base class for all file system nodes"""
    
    def __init__(self, name: str, node_type: NodeType, parent: Optional['BaseNode'] = None):
        self.name = name
        self.type = node_type
        self.parent = parent
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.size = 0  # bytes
        self.access_mode = "Read / Write"
    
    def get_path(self) -> str:
        """Get absolute path of this node"""
        if self.parent is None:
            return "/" + self.name if self.name != "" else "/"
        parent_path = self.parent.get_path()
        if parent_path == "/":
            return "/" + self.name
        return parent_path + "/" + self.name
    
    def update_modified(self):
        """Update the modified timestamp"""
        self.modified_at = datetime.now()
    
    def format_size(self) -> str:
        """Format size in human-readable format"""
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f} KB"
        else:
            return f"{self.size / (1024 * 1024):.1f} MB"


class FileNode(BaseNode):
    """Represents a file in the file system"""
    
    def __init__(self, name: str, parent: Optional[BaseNode] = None, size: int = 0):
        super().__init__(name, NodeType.FILE, parent)
        self.size = size
        self.extension = name.split('.')[-1] if '.' in name else ""
    
    def get_file_type(self) -> str:
        ext = self.extension.lower()
        type_map = {
            'pdf': 'PDF Document',
            'doc': 'Word Document',
            'docx': 'Word Document',
            'txt': 'Text Document',
            'png': 'PNG Image',
            'jpg': 'JPEG Image',
            'jpeg': 'JPEG Image',
            'mp3': 'Audio File',
            'mp4': 'Video File'
        }
        if ext in type_map:
            return type_map[ext]
        elif ext:
            return f"{ext.upper()} File"
        return "Unknown File Type"
        
    def __repr__(self):
        return f"FileNode({self.name}, {self.format_size()})"


class DirectoryNode(BaseNode):
    """Represents a directory in the file system"""
    
    def __init__(self, name: str, parent: Optional[BaseNode] = None):
        super().__init__(name, NodeType.DIRECTORY, parent)
        self.children: Dict[str, BaseNode] = {}
    
    def add_child(self, node: BaseNode) -> bool:
        """Add a child node to this directory"""
        if node.name in self.children:
            return False
        self.children[node.name] = node
        node.parent = self
        self.update_modified()
        return True
    
    def remove_child(self, name: str) -> bool:
        """Remove a child node from this directory"""
        if name not in self.children:
            return False
        del self.children[name]
        self.update_modified()
        return True
    
    def get_child(self, name: str) -> Optional[BaseNode]:
        """Get a child node by name"""
        return self.children.get(name)
    
    def has_child(self, name: str) -> bool:
        """Check if a child exists"""
        return name in self.children
    
    def is_empty(self) -> bool:
        """Check if directory is empty"""
        return len(self.children) == 0
    
    def get_depth(self) -> int:
        """Get the depth of this directory from root"""
        depth = 0
        current = self.parent
        while current is not None:
            depth += 1
            current = current.parent
        return depth
    
    def __repr__(self):
        return f"DirectoryNode({self.name}, {len(self.children)} children)"
