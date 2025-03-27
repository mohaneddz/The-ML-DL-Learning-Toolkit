import os
import sys
import nbformat
from nbconvert import PythonExporter
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_notebook_to_python(notebook_path, output_path=None):
    """
    Convert a Jupyter notebook to a Python file.
    
    Args:
        notebook_path (str): Path to the Jupyter notebook file
        output_path (str, optional): Path where the Python file will be saved.
                                    If None, replaces .ipynb with .py
    
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    if output_path is None:
        output_path = os.path.splitext(notebook_path)[0] + '.py'
    
    try:
        # Read the notebook
        with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
            notebook_content = nbformat.read(notebook_file, as_version=4)
        
        # Configure the exporter - use default Python template
        python_exporter = PythonExporter()
        
        # Convert the notebook to Python
        python_code, _ = python_exporter.from_notebook_node(notebook_content)
        
        # Add a header comment showing the source notebook
        header = f"# Converted from: {os.path.basename(notebook_path)}\n\n"
        python_code = header + python_code
        
        # Write the Python code to the output file
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(python_code)
        
        return True
    
    except Exception as e:
        logger.error(f"Error converting {notebook_path}: {str(e)}")
        return False

def process_directory(directory='.'):
    """
    Recursively process all directories and convert all notebooks.
    
    Args:
        directory (str): Directory to start from
    
    Returns:
        tuple: (success_count, fail_count)
    """
    success_count = 0
    fail_count = 0
    
    logger.info(f"Processing directory: {os.path.abspath(directory)}")
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb'):
                notebook_path = os.path.join(root, file)
                
                # Skip checkpoint files
                if '.ipynb_checkpoints' in notebook_path:
                    continue
                
                logger.info(f"Converting: {notebook_path}")
                
                if convert_notebook_to_python(notebook_path):
                    success_count += 1
                    logger.info(f"Successfully converted: {notebook_path}")
                else:
                    fail_count += 1
                    logger.warning(f"Failed to convert: {notebook_path}")
    
    return success_count, fail_count

if __name__ == "__main__":
    # Get the starting directory from command line arguments or use current directory
    start_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    logger.info("Starting notebook conversion process")
    success, fail = process_directory(start_dir)
    logger.info(f"Conversion complete. Successfully converted: {success}, Failed: {fail}")