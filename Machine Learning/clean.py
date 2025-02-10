import os
import nbformat # type: ignore

def remove_code_cells_from_notebook(notebook_path):
    """Remove all code cells from a Jupyter notebook."""
    with open(notebook_path, 'r', encoding='utf-8') as file:
        notebook = nbformat.read(file, as_version=4)

    # To Remove all code cells :)
    notebook.cells = [cell for cell in notebook.cells if cell.cell_type != 'code']

    # Save the modified notebook
    with open(notebook_path, 'w', encoding='utf-8') as file:
        nbformat.write(notebook, file)

def process_directory(directory_path):
    """Process all .ipynb files in the given directory and its subdirectories."""
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith('.ipynb'):
                notebook_path = os.path.join(root, filename)
                print(f"Processing {notebook_path}...")
                remove_code_cells_from_notebook(notebook_path)
                print(f"Finished processing {notebook_path}")

if __name__ == "__main__":
    # Get the current directory to do the deeds
    current_directory = os.getcwd()
    process_directory(current_directory)
