# dana
SDK for DANA API (https://dashboard.dana.id/api-docs) 

## Requirements.

Python 3.9.1+

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import dana.payment_gateway.v1
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import dana.payment_gateway.v1
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then go to documentation per API you wanna use:

## Documentation for API Endpoints

API | Description
------------- | -------------
[**PaymentGatewayApi**](docs/payment_gateway/v1/PaymentGatewayApi.md) | API for doing operations in DANA Payment Gateway (Gapura)

