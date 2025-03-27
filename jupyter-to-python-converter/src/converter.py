def convert_notebooks_to_python(directory):
    import os
    import nbformat
    from nbconvert import PythonExporter

    def is_notebook(file_name):
        return file_name.endswith('.ipynb')

    def save_python_file(notebook_path, python_code):
        python_file_path = notebook_path.replace('.ipynb', '.py')
        with open(python_file_path, 'w', encoding='utf-8') as f:
            f.write(python_code)

    for root, _, files in os.walk(directory):
        for file in files:
            if is_notebook(file):
                notebook_path = os.path.join(root, file)
                with open(notebook_path, 'r', encoding='utf-8') as f:
                    notebook_content = nbformat.read(f, as_version=4)
                python_exporter = PythonExporter()
                python_code, _ = python_exporter.from_notebook_node(notebook_content)
                save_python_file(notebook_path, python_code)