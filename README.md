# Hit Count Lambda 

## Description
This AWS Lambda function acts as a backend service designed to update a user hitcount stored in a database. It is a pivotal component within a larger architecture developed as part of [The Cloud Resume Challenge](https://cloudresumechallenge.dev/). Triggered via API, it increments the hitcount value by 1.

![](TODO.png)

The backing database is DynamoDB.

## Functionality
- Increment the hitcount value by 1.

## Getting Started
This project uses [Poetry](https://python-poetry.org/docs/#installation) for dependency management. 

To install `pipx` on macOS:
```
brew install pipx
pipx ensurepath
```
Then use `pipx`: 
```
pipx install poetry
```

Clone this repository, then create a Python [Virtual Environment](https://docs.python.org/3/tutorial/venv.html) inside the directory and activate it by running:
```
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies with:
```
make install-dependencies
```

## Development
Upgrade or add any dependencies with:
```
make upgrade-dependencies
```

Code linting is done with `flake8` and `isort`. Run linting with:
```
make lint
``` 

Run the unit tests with:
```
make test
```

## Build
The function is packaged for deployment in a zip file named `artifact.zip`. Create this with:
```
make build
```
The artifact file will created in the home directory.

## Deployment
As part of the Cloud Resume Challenge project, this function (the artifact zip file) is deployed using Terraform. The code for that can be found here. #TODO add link

## Environment Variables
The function references two environment variables:
- LOG_LEVEL: For logging (Optional: Defaults to INFO)
- HITS_TABLE_NAME: The DynamoDB table name. (Required)

## Configuration


## License
This project and its Terraform modules are released under the MIT License. See
the bundled [LICENSE](LICENSE.md) file for details.
