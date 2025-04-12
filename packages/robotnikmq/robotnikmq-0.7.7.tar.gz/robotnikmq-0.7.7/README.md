# RobotnikMQ

Utilities for safe, efficient, and scalable infrastructure using RabbitMQ

## Usage

TODO

## Installation & Setup

To install robotnikmq with [`pip`](https://pip.pypa.io/en/stable/) execute the following:

```bash
pip install robotnikmq
```

### Configuration

RobotnikMQ can be configured globally, on a per-user, or on a per-application basis. When certain functions of the RobotnikMQ library are called without a provided configuration, it will attempt to find a configuration first for the application in the current working directory `./robotnikmq.yaml`, then for the user in `~/.config/robotnikmq/robotnikmq.yaml` and then for the system in `/etc/robotnikmq/robotnikmq.yaml`. An error will be raised if a configuration is not provided and neither of those files exist.

The RobotnikMQ configuration is primarily a list of servers organized into tiers. If a given system or user can be expected to connect to the same cluster the vast majority of the time, then you can/should use a per-user or global configuration. Otherwise, simply have your application configure its own RobotnikMQ configuration (see **Usage** section).

The configuration file itself should look something like this:

```yaml
tiers:
- - ca_cert: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/robotnik-ca.crt
    cert: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/issued/rabbitmq-vm/rabbitmq-vm.crt
    host: 127.0.0.1
    key: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/issued/rabbitmq-vm/rabbitmq-vm.key
    password: ''
    port: 1
    user: ''
    vhost: ''
  - ca_cert: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/robotnik-ca.crt
    cert: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/issued/rabbitmq-vm/rabbitmq-vm.crt
    host: '1'
    key: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/issued/rabbitmq-vm/rabbitmq-vm.key
    password: '1'
    port: 1
    user: '1'
    vhost: '1'
- - ca_cert: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/robotnik-ca.crt
    cert: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/issued/rabbitmq-vm/rabbitmq-vm.crt
    host: 127.0.0.1
    key: /home/eugene/Development/robotnikmq/tests/integration/vagrant/pki/issued/rabbitmq-vm/rabbitmq-vm.key
    password: hackme
    port: 5671
    user: robotnik
    vhost: /robotnik
```

In the example above, you should be able to see two tiers of servers, the first has two server configurations that are intentionally broken for testing purposes, while the second has a valid configuration (this is the configuration that is used for unit-testing).

The idea is that RobotnikMQ will first attempt to connect to all servers in the first tier in a random order, then if all of them fail, it will attempt to connect to all the servers in the second tier, and so on. This is intended to allow both load-balancing on different servers and for redundancy in case some of those servers fail. You can also configure only one tier with one server, or just a list of tiers, each of which have one server in them. This way, the secondary and tertiary servers would only be used if there is something wrong with the primary.

## Development

### Standards

- Be excellent to each other
- Code coverage must be at 100% for all new code, or a good reason must be provided for why a given bit of code is not covered.
  - Example of an acceptable reason: "There is a bug in the code coverage tool and it says its missing this, but its not".
  - Example of unacceptable reason: "This is just exception handling, its too annoying to cover it".
- The code must pass the following analytics tools. Similar exceptions are allowable as in rule 2.
  - `pylint --disable=C0103,C0111,W1203,R0903,R0913 --max-line-length=120 ...`
  - `flake8 --max-line-length=120 ...`
  - `mypy --ignore-missing-imports --follow-imports=skip --strict-optional ...`
- All incoming information from users, clients, and configurations should be validated.
- All internal arguments passing should be typechecked during testing with [`typeguard.typechecked`](https://typeguard.readthedocs.io/en/latest/userguide.html#using-the-decorator) or [the import hook](https://typeguard.readthedocs.io/en/latest/userguide.html#using-the-import-hook).

### Development Setup

Using [pdm](https://pdm.fming.dev/) install from inside the repo directory:

```bash
pdm install
```

This will install all dependencies (including dev requirements) in a [PEP582-compliant project](https://pdm.fming.dev/latest/usage/pep582/) which you can always run specific commands with `pdm run ...`.

#### IDE Setup

**Sublime Text 3**

```bash
curl -sSL https://gitlab.com/-/snippets/2385805/raw/main/pdm.sublime-project.py | pdm run python > robotnikmq.sublime-project
```

**VSCodium/VSCode**

I recommend installing the [pdm-vscode](https://github.com/frostming/pdm-vscode) plug-in:

```bash
sudo pdm plugin add pdm-vscode
```

## Testing

All testing should be done with `pytest` which is installed with the `dev` requirements.

To run all the unit tests, execute the following from the repo directory:

```bash
pdm run pytest --runslow
```

Removing the `--runslow` parameter will cause it to skip tests that have been marked with `@pytest.mark.slow`

This should produce a coverage report in `/path/to/dewey-api/htmlcov/`

While developing, you can use [`watchexec`](https://github.com/watchexec/watchexec) to monitor the file system for changes and re-run the tests:

```bash
watchexec -r -e py,yaml pdm run pytest
```

To run a specific test file:

```bash
pdm run pytest tests/unit/test_core.py
```

To run a specific test:

```bash
pdm run pytest tests/unit/test_core.py::test_hello
```

For more information on testing, see the `pytest.ini` file as well as the [documentation](https://docs.pytest.org/en/stable/).

### Integration Testing

For integration testing, this code uses [testcontainers-rabbitmq](https://testcontainers-python.readthedocs.io/en/latest/rabbitmq/README.html). In order to enable this, you will need to install docker, and ensure that your user has the ability to interact with the docker service:

```bash
sudo apt install docker
sudo groupadd docker # may fail if the docker group already exists
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world # verify that everything is working well
```

We also have tests that do more complex things, such as `tests/integration/test_broadcast.py::test_confirm_subscriber_reconnection_behavior_on_node_failure` which rely on the [Python Docker SDK](https://docker-py.readthedocs.io/en/stable/index.html), but that needs docker installed as well.

### Python Version Support

RobotnikMQ also has Tox configured for all supported versions of python so that we can verify that it works with all of them. This is defined in the `tox.ini` file and all tests can be run with:

```bash
tox run
```