# automate_ghiseul_ro

This script automates the process of logging into the Ghiseul.ro website and downloading payment receipts.

## Requirements

- Python 3.x
- Google Chrome
- ChromeDriver
- A `.env` file with the following variables:
  - `GHISEULRO_URL`: The URL of the Ghiseul.ro login page
  - `GHISEULRO_USERNAME`: Your Ghiseul.ro username
  - `GHISEULRO_PASSWORD`: Your Ghiseul.ro password

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/fotoalin/automate_ghiseul_ro.git
    cd automate_ghiseul_ro
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project directory and add your credentials:
    ```env
    GHISEULRO_URL=https://www.ghiseul.ro/ghiseul/public
    GHISEULRO_USERNAME=your_username
    GHISEULRO_PASSWORD=your_password
    ```

5. Ensure you have Google Chrome installed and download the corresponding ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). Place the `chromedriver` executable in your PATH or in the project directory.

## Usage

Run the script to log in to Ghiseul.ro and download the receipts:
```sh
python download_receipts.py
```

The receipts will be downloaded to the `docs` folder in the project directory.

## Logging

The script uses Python's `logging` module to log information and errors. Logs will be printed to the console.

## License

This project is licensed under the MIT License.
