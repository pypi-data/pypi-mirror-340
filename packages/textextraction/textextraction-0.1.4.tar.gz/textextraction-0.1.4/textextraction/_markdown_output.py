import os
import logging
from datetime import datetime

class MarkdownOutput:
    """
    Utility class for formatting and saving text content as markdown files.
    """
    
    def __init__(self, add_metadata=True):
        """
        Initialize the markdown output processor.
        
        Args:
            add_metadata (bool): Whether to add metadata to the output file.
        """
        self.add_metadata_flag = add_metadata
        self.logger = logging.getLogger(__name__)
    
    def add_metadata(self, text, title=None, source_file=None):
        """
        Add YAML metadata to the markdown file.
        
        Args:
            text (str): The text content.
            title (str): Optional title for the document.
            source_file (str): Optional source file path.
            
        Returns:
            str: Text with metadata header.
        """
        if not self.add_metadata_flag:
            return text
            
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not title and source_file:
            title = os.path.basename(source_file)
            
        metadata_lines = [
            "---",
            f"date: {now}",
        ]
        
        if title:
            metadata_lines.append(f"title: {title}")
            
        if source_file:
            metadata_lines.append(f"source: {source_file}")
            
        metadata_lines.append("---\n\n")
        
        return "\n".join(metadata_lines) + text
    
    def save_markdown(self, text, output_path, title=None, source_file=None):
        """
        Save text content as a markdown file with optional metadata.
        
        Args:
            text (str): The text content to save.
            output_path (str): Path to save the markdown file.
            title (str, optional): Title for the document.
            source_file (str, optional): Source file path.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Add metadata if requested
            if self.add_metadata_flag:
                text = self.add_metadata(text, title, source_file)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Save the file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
                
            self.logger.info(f"Markdown file saved to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving markdown file: {e}")
            return False 