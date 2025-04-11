# Hacking guide for developers

## Prerequisites

- Python >= 3.9

## CLI development

### Create a dev environment

It is strongly suggested to use a dedicated Python Virtual Environment do develop the EF Portal CLI. Start by creating and activating an empty virtual env with:

```bash
python -m venv /path/to/new/venv
source /path/to/new/venv/bin/activate
```

where `/path/to/new/venv` is the directory where the new Virtual Environment will be created.

With you dev environment activated, use the following command to easily install all the libraries needed to build, run and publish to PyPI:

```bash
pip install -r $PROJECT_ROOT/requirements.txt
```

where `$PROJECT_ROOT` is the directory where you checked out the code.
`requirements.txt` is constantly updated moving forward in the development process, so be sure to run again the command above if you experience any error during development.

For more information about Python Virtual Environments, check the official doc [here](https://docs.python.org/3/tutorial/venv.html).

You can safely remove a Virtual Environment anytime, just delete the Virtual Environment folder you created.

### Run the CLI without installing

`efpclient` startup script is automatically created by `pip install` for a standard installation.
The `$PROJECT_ROOT/efpclient` script is provided to ease the startup of the CLI without the need of installing it everytime before testing changes.

`cd` into the directory where you checked out the code and type

```bash
./efpclient
```

to execute the CLI.

### Run code linting check

`cd` into the directory where you checked out the code and type

```bash
pylint src
```

New code must not introduce any linting issue before being merged to mainline.

### Test CLI installation

Create a new, empty Virtual Environment to better simulate a customer, non dev environment:

```bash
python -m venv /path/to/test/venv
source /path/to/test/venv/bin/activate
```

Then `cd` into the directory where you checked out the code and type

```bash
pip install .
```

to perform the installation. If everything goes fine, you will be able to execute the EF Portal CLI, being in the Virtual Environment, simply typing

```bash
efpclient
```

You are encouraged to check CLI dependencies automatically installed by `pip`. The output of:

```bash
pip freeze
```

should show only packages listed in the `dependencies` definition under the `[project]` section of `pyproject.toml`, apart from `efpclient` itself.

### Build the CLI before publishing

`cd` into the directory where you checked out the code and type:

```bash
python -m build
```

If everything goes fine, you will see built artifacts in the `dist` directory. You can also check built artifacts using:

```bash
twine check dist/*
```

### Publish the CLI to PyPI

Please refer to the official documentation [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives)

### How to update `pyproject.toml` dependencies and `requirements.txt` file

`requirements.txt` is created starting from a Python 3.9.19 installation, which is the latest 3.9 version available, in order to make the dev environment fully compliant with Python 3.9.
When `requirements.txt` needs to be updated due to a new library, it is strongly suggested to do this in a Python 3.9.19 environment.

You can easily install Python 3.9.19 using [pyenv](https://github.com/pyenv/pyenv):

```bash
pyenv install 3.9.19
```

You can then create a new Python 3.9 env, activate it, init with the old `requirments.txt` and install the new library.

Let's say we want to use the library `newlib` in the project, we do:

```bash
pyenv shell 3.9.19
python -m venv /path/to/new/venv
source /path/to/new/venv/bin/activate
pip install -r $PROJECT_ROOT/requirements.txt
pip install newlib
```

where `$PROJECT_ROOT` is the directory where you checked out the code.

Finally, update the `requirements.txt` file using:

```bash
pip freeze > $PROJECT_ROOT/requirements.txt
```

and add the `newlib` version in `pyproject.toml` as found in `requirements.txt`

### Update auto-generated Swagger client

Every time the EF Portal REST API model changes, the auto-generated Swagger client needs to be updated to reflect any API change.

Auto-generated swagger client is located in `$PROJECT_ROOT/src/efpclient/swagger_client` directory, where `$PROJECT_ROOT` is the directory where you checked out the code.

#### Requirements

- [Swagger Codegen v3](https://swagger.io/tools/swagger-codegen/)
  - On mac, just use `brew install swagger-codegen`

#### How to

In order to update it you need to:

- Delete the old Swagger client

```bash
rm -rf $PROJECT_ROOT/src/efpclient/swagger_client
```

- Download the updated OpenAPI model from a running EF Portal instance

```bash
curl -k -X GET http(s)://<efphost>:<port>/enginframe/rest/openapi.json -o $HOME/openapi.json
```

where `<efphost>:<port>` is the address of your target EF Portal instance

- Build the updated Swagger client

```bash
swagger-codegen generate \
    -i $HOME/openapi.json \
    -l python \
    -o $HOME/python_swagger \
    -DpackageName="efpclient.swagger_client"
```

- Copy the swagger client in the EF Portal Client code

```bash
cp -rp $HOME/python_swagger/efpclient/swagger_client $PROJECT_ROOT/src/efpclient/
```
