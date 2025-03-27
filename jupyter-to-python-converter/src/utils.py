def is_notebook(file_path):
    """Check if the given file is a Jupyter notebook."""
    return file_path.endswith('.ipynb')

def save_python_file(content, output_path):
    """Save the converted Python content to a file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)