# FlaskCMDB

FlaskCMDB is a simple Configuration Management Database (CMDB) application built with Flask. It allows users to manage and track configuration items (CIs) within their IT environment.

## Features

- Add, update, and delete configuration items
- Search and filter configuration items
- User authentication and authorization
- RESTful API for integration with other systems

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/FlaskCMDB.git
    cd FlaskCMDB
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. Run the application:
    ```sh
    flask run
    ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000`.
2. Register a new user account or log in with an existing account.
3. Start managing your configuration items.



## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.
