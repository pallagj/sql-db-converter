# SQL DB  Converter to excel and from excel

SQL-to-Excel Converter is a simple Streamlit application that allows you to generate Excel files from SQL database tables. The application connects to the database, runs SQLselect queries to get data from specified tables, and then exports the data into an Excel file.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/pallagj/sql-db-converter.git
    ```

2. Move into the project directory:
    ```bash
    cd sql-db-converter
    ```

3. Install the necessary packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:
    ```bash
    python -m streamlit run .\app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` or the URL shown in your CLI.

3. Enter your SQL connection parameters.

4. Test the SQL connection.

5. Enter the names of the tables you want to export, one per line.

6. Enter the names of any fields you wish to exclude from the Excel file, one per line.

7. Enter the desired name for the Excel file.

8. Click the "Generate" button to generate the Excel file.

## Requirements

- Python 3.6+
- Streamlit
- pandas
- SQLAlchemy
- openpyxl
- pymysql

Note: For a complete list of requirements, see the `requirements.txt` file.
