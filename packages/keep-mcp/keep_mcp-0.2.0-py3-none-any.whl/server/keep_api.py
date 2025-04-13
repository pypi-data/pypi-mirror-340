import gkeepapi
import os
from dotenv import load_dotenv

_keep_client = None

def get_client():
    """
    Get or initialize the Google Keep client.
    This ensures we only authenticate once and reuse the client.
    
    Returns:
        gkeepapi.Keep: Authenticated Keep client
    """
    global _keep_client
    
    if _keep_client is not None:
        return _keep_client
    
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    email = os.getenv('GOOGLE_EMAIL')
    master_token = os.getenv('GOOGLE_MASTER_TOKEN')
    
    if not email or not master_token:
        raise ValueError("Missing Google Keep credentials. Please set GOOGLE_EMAIL and GOOGLE_MASTER_TOKEN environment variables.")
    
    # Initialize the Keep API
    keep = gkeepapi.Keep()
    
    # Authenticate
    keep.authenticate(email, master_token)
    
    # Store the client for reuse
    _keep_client = keep
    
    return keep

def serialize_note(note):
    """
    Serialize a Google Keep note into a dictionary.
    
    Args:
        note: A Google Keep note object
        
    Returns:
        dict: A dictionary containing the note's id, title, text, pinned status, color and labels
    """
    return {
        'id': note.id,
        'title': note.title,
        'text': note.text,
        'pinned': note.pinned,
        'color': note.color.value if note.color else None,
        'labels': [{'id': label.id, 'name': label.name} for label in note.labels.all()]
    }

def can_modify_note(note):
    """
    Check if a note can be modified based on label and environment settings.
    
    Args:
        note: A Google Keep note object
        
    Returns:
        bool: True if the note can be modified, False otherwise
    """
    unsafe_mode = os.getenv('UNSAFE_MODE', '').lower() == 'true'
    return unsafe_mode or has_keep_mcp_label(note)

def has_keep_mcp_label(note):
    """
    Check if a note has the keep-mcp label.
    
    Args:
        note: A Google Keep note object
        
    Returns:
        bool: True if the note has the keep-mcp label, False otherwise
    """
    return any(label.name == 'keep-mcp' for label in note.labels.all()) 