# jupyter-to-python-converter

## Overview
The Jupyter to Python Converter is a utility that recursively converts Jupyter notebooks (.ipynb files) into Python scripts (.py files). This project leverages the `nbconvert` library to facilitate the conversion process.

## Project Structure
```
jupyter-to-python-converter
├── src
│   ├── converter.py       # Main conversion logic
│   └── utils.py          # Utility functions
├── tests
│   └── test_converter.py  # Unit tests for the converter
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Installation
To install the required dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage
To convert Jupyter notebooks to Python files, you can run the `converter.py` script. Make sure to specify the directory containing the notebooks you wish to convert.

Example command:

```
python src/converter.py <path_to_notebooks>
```

Replace `<path_to_notebooks>` with the path to the directory containing your Jupyter notebooks.

## Testing
To run the unit tests for the conversion logic, navigate to the `tests` directory and execute:

```
pytest test_converter.py
```

Ensure that you have `pytest` installed as part of your requirements.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.