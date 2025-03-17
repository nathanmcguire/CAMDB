# Configuration and Asset Management Database

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
    # macOS / Linux
    source venv/bin/activate
    # Windows
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    .\venv\Scripts\activate
    ```

3. Install the dependencies:
    ```sh
    pip3 install -r requirements.txt
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
    #or
    python3 run.py
    ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000`.
2. Register a new user account or log in with an existing account.
3. Start managing your configuration items.

## Feature ideas
- Focus on CIS Controls
- Leverage API's to bring in data from systems like Active Directory, Service Desk Plus, Meraki, and vSphere
- Assets, Configurations, Changes across environment
- Alerting and reporting unauthorized config changes, asset lifecycle tracking
- RBAC user levels
- CLI/API
- SSO Azure Ad



## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact the repository owner.
