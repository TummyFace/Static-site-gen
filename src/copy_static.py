import os
import shutil
import logging

logger = logging.getLogger(__name__)

def copy_directory_recursive(src, dest):
    """
    Recursively copy all contents from source directory to destination directory.
    First deletes all contents of the destination directory to ensure a clean copy.
    
    Args:
        src (str): Source directory path
        dest (str): Destination directory path
    """
    # Delete destination directory if it exists
    if os.path.exists(dest):
        logger.info(f"Deleting existing destination directory: {dest}")
        shutil.rmtree(dest)
    
    # Create the destination directory
    os.mkdir(dest)
    logger.info(f"Created destination directory: {dest}")
    
    # Recursively copy all files and directories
    for filename in os.listdir(src):
        src_path = os.path.join(src, filename)
        dest_path = os.path.join(dest, filename)
        
        if os.path.isfile(src_path):
            # Copy file
            shutil.copy(src_path, dest_path)
            logger.info(f"Copied file: {src_path} -> {dest_path}")
        else:
            # Recursively copy directory
            copy_directory_recursive(src_path, dest_path)
