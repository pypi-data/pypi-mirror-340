# PandaPlotDocs

A simple Python library to generate a PDF reference document containing essential functions and methods for Pandas and Matplotlib.

## Installation

Ensure you have Python 3.8+ installed.

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repo-url>
    cd pandaplotdocs
    ```

2.  **Install the package:**
    It's recommended to install in a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    pip install .
    ```
    Alternatively, if you want to install it in editable mode (useful for development):
    ```bash
    pip install -e .
    ```
    This installs the necessary dependencies (`fpdf2`).

## Usage

Import the library and call the `generate_docs_pdf` function:

```python
import pandaplotdocs

# Generate the PDF in the current directory with the default name
pandaplotdocs.generate_docs_pdf()

# Or specify a different output path/filename
# pandaplotdocs.generate_docs_pdf(output_filename="my_reference.pdf")

print("PDF reference generated!")
```

This will create a file named `essential_plotting_docs.pdf`

## Contributing

Feel free to add more functions, improve descriptions, or enhance the PDF layout.

## License

This project is licensed under the MIT License