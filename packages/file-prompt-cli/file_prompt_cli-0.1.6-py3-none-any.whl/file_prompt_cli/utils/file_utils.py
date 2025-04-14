import os
import glob
from pathlib import Path
from typing import List, Union, Optional
import magic
from rich.progress import Progress

class FileUtils:
    """Utility class for file operations."""
    
    @staticmethod
    def expand_glob_patterns(patterns: Union[str, List[str]]) -> List[Path]:
        """Expand glob patterns into list of file paths."""
        if isinstance(patterns, str):
            patterns = [patterns]
            
        files = []
        for pattern in patterns:
            # Convert to absolute path if needed
            if not os.path.isabs(pattern):
                pattern = os.path.abspath(pattern)
                
            # Expand glob pattern
            matches = glob.glob(pattern, recursive=True)
            files.extend([Path(match) for match in matches])
            
        return files
    
    @staticmethod
    def validate_file(file_path: Path) -> bool:
        """Validate if a file exists and is accessible."""
        try:
            return file_path.exists() and file_path.is_file() and os.access(file_path, os.R_OK)
        except Exception:
            return False
    
    @staticmethod
    def get_file_size(file_path: Path) -> int:
        """Get file size in bytes."""
        return os.path.getsize(file_path)
    
    @staticmethod
    def get_mime_type(file_path: Path) -> str:
        """Get MIME type of a file."""
        mime = magic.Magic(mime=True)
        return mime.from_file(str(file_path))
    
    @staticmethod
    def is_supported_file_type(file_path: Path) -> bool:
        """Check if file type is supported."""
        mime_type = FileUtils.get_mime_type(file_path)
        supported_types = {
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain',
            'image/jpeg',
            'image/png',
            'image/webp'
        }
        return mime_type in supported_types
    
    @staticmethod
    def get_file_extension(file_path: Path) -> str:
        """Get file extension."""
        return file_path.suffix.lower()
    
    @staticmethod
    def create_temp_file(content: bytes, extension: Optional[str] = None) -> Path:
        """Create a temporary file with given content."""
        import tempfile
        suffix = f".{extension}" if extension else ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp.write(content)
            return Path(temp.name)
    
    @staticmethod
    def cleanup_temp_files(files: List[Path]) -> None:
        """Clean up temporary files."""
        for file in files:
            try:
                if file.exists():
                    file.unlink()
            except Exception:
                pass
    
    @staticmethod
    def process_files_with_progress(files: List[Path], callback, description: str = "Processing files") -> List[Any]:
        """Process files with progress bar."""
        results = []
        with Progress() as progress:
            task = progress.add_task(description, total=len(files))
            for file in files:
                result = callback(file)
                results.append(result)
                progress.update(task, advance=1)
        return results 