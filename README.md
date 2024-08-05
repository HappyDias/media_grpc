# Cyrex Vacancies GRPC load test

This code load tests the Cyrex Vacancies API

## Description

This code leverages the following tools:
1. [grpc](https://grpc.io/docs/languages/python/) - Client library generation and communication
2. [locust](https://docs.locust.io/en/stable/) - Load testing tool
3. [grpc_interceptor](https://grpc-interceptor.readthedocs.io/en/latest/) - For 'middleware' purposes
4. [grpcio-tools](https://grpc.io/docs/languages/python/quickstart/) - Protobuff code generation

## Requirements

1. Python 3.11+ - Should work in other versions, was not tested though

Code was run and tested exclusively in Windows, please feel free to point out issues in other Unix-based OS

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/HappyDias/media_grpc.git
    ```
2. Navigate to the project directory:
    ```sh
    cd media_grpc
    ```
3. (Optional) Create a virtual environment
    ```sh
    python -m venv 
    ```
4. Build the project (assuming you have a build script or instructions):
    ```sh
    pip install -r requirements.txt
    ```
5. Place the user authentication file `auth.json` in the root of the folder. Use the file `auth-template.json` for reference

## Usage

To start the load test, run the following command:
```sh
locust --headless --csv <stats_file_prefix> --config-users locust_users.json -u <Number_of_users>
```

Where `stats_file_prefix` is the name prefix you would like to have on the output files

## Output
The output of the code is a set of csv files:
1. `<stats_file_prefix>_exceptions.csv` - List of ocurred exceptions, including stack traces
2. `<stats_file_prefix>_failures.csv` - List of RPC failures. 
3. `<stats_file_prefix>_stats_history.csv` - List of statistics during the course of the load test
4. `<stats_file_prefix>_stats.csv` - List of latest stats retrieved from the test

The test will periodically update the files as the tests goes on.

## Questions

Please create a PR with change suggestions or just to start a conversation using the issues tab