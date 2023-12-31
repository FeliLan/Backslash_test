# Backslash_test
## a test framework for the following repo https://github.com/NeerChayaphon/TodoList-API-With-Go.git
## Installation

1. Clone the service repo 
   and follow the README file

    ```bash
    git clone https://github.com/NeerChayaphon/TodoList-API-With-Go.git
    ```

2. Clone my repository:

    ```bash
    git clone https://github.com/FeliLan/Backslash_test.git
    cd Backslash_test
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On Unix or MacOS:

        ```bash
        source venv/bin/activate
        ```

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running Tests

To run the tests, use the following command:

in the config.py enter the url that you are running the service on

```bash
pytest
```