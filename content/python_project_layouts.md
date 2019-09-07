Title: Python Project Layout For Flask and Everything
Date: 2019-09-03 10:20
Modified: 2019-09-03 10:20
Category: Python
Tags: python, flask, docker
Slug: python-project-layout
Authors: Rishi Maker
Summary: Python Project Laoyouts.


I will walk through a minimal python flask application to highlight the project layout approach I took.

The driving factor is co-developing a self-contained library class along with the main application

## Summary

I will highlight the following areas using a sample project which can be found [here](https://github.com/cmlzaGk/sampleflask)

- Project layout.
- setup.py, \_\_init\_\_.py and requirements.txt
- Intra-package and inter package references.
- Class factories
- Test cases and code coverage
- DockerFiles

## Project Layout

The project layout looks like this.

```bash
.
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.unittests
├── requirements.txt
├── run_coverage.sh
├── uwsgi.ini
└──-bettermath-lib
    ├── setup.py
    └── bettermathlib
        ├── better_random.py
        ├── __init__.py
    └── bettermathlib_tests
        ├── tests_bettermathlib.py
        ├── __init__.py
└── randomweb-app
    ├── setup.py
    └── randomwebapp_tests
        ├── tests_basic.py
        ├── tests_client.py
        ├── __init__.py
    └── randomweb_app
        ├── config.py
        ├── create_app.py
        ├── flask_app.py
        ├── random_creator.py
        ├── __init__.py
        └── main
            ├── views.py
            ├── __init__.py
            └── static
                ├── about.txt
            └── templates
                ├── base.html
                └── betterrandom.html
```

A distribution is a folder that can be installed and moved around anywhere.  bettermath-lib and randomweb-app are the self-contained distributions.

A package is a directory contains other packages or modules and is also called "Import Package" because its importable.

The file \_\_init\_\_.py is a special file that is executed when a package is imported in the runtime.

Here bettermpathlib, bettermathlib\_tests are packages inside distribution bettermath-lib. randomweb\_app and randomwebapp\_tests are packages inside distribution randomweb-app, and finally main is a package inside package randomweb\_app.


## setup.py, \_\_init\_\_.py and requirements.txt

The three files play a significant role in app development.

setup.py is part of setuptools and defines properties of a distribution.

```python
from setuptools import setup, find_packages

setup(
    name='randomweb-app',
    version='1.0',
    description='Random Webapp',
    author='Fishy Baker',
    author_email='fishybaker@hotmail.com',
    packages=find_packages(),
    install_requires = [
        'Flask >= 1.1.1',
        'Flask-Bootstrap >= 3.3.7.1',
        'Flask-WTF >= 0.14.2',
        'jsonschema >= 3.0.1',
        'bettermath-lib >= 1.0'
    ],
    include_package_data=True,
    package_data={'randomweb_app': ['templates/*', 'static/*']}
)
```

There are three main parts of setup.py

```python
    packages=find_packages(),
```

find\_packages is a neat helper to automatically include all packages inside randomweb-app as part of the distributable. The other option would be to create a static python list with a list of packages.

```python
    include_package_data=True,
    package_data={'randomweb_app': ['templates/*', 'static/*']}
```

By default non python files aka data files are excluded in a package. This is a good place to include them, and they can continue to be referenced by their relative paths anywhere.

Before, we go over install\_requires, lets talk about requirements.txt. requirements.txt is created typically by using the pip freeze command in your virtual env.

```bash
pip freeze > requirements.txt
```

Hence requirements.txt represents the distributions that the application was tested under. It will have specific versions of external distributions.

The purpose of requirements.txt is to ensure that the production environments are run against specific versions.

However, it is not part of a distribution, because when we distribute, we would like consumers to obtain the latest and greatest versions of packages like Flask.

In the distribution, the minimum version the package works with is defined, and that is where install\_requires in setup.py comes in.

Finally a word on \_\_init\_\_.py.  \_\_init\_\_.py plays a crucial role in namespacing the package's contents appropriately.

The class BetterRandom is in module better\_random.py. So a consumer of my distribution would have to import bettermathlib.better\_random to access BetterRandom. This is not optimal.

By directly importing BetterRandom in \_\_init\_\_.py we bring BetterRandom to bettermathlib namespace, and then "import bettermathlib" is good enough to access BetterRandom.

```python
from .better_random import BetterRandom
```


## Intra-package and inter package references.

References is now where we will see the advantage of keeping packages distributable come in.

Pip has an option \-e, called the editable option, using which pip will reference the local source paths in the deployment index.

```bash
pip install  --no-deps -e bettermath-lib/
pip install  --no-deps -e randomweb-app/
```

After this both the packages are self-contained and installed in the dev environment. We can continue to make code changes without re-installing the packages.

For referencing modules within a package, we will use the intra-package references :

```python
from ..random_creator import random_int
```

For inter-package references, we can now use absolute references without worrying about where the actual code for the package resides.

```python
from bettermathlib import BetterRandom
```

Since we used pip to deploy the two distributions, we want to exclude these distributions in the applications requirements.txt. Instead, we will deploy all co-developed distributions seperately in production.

```bash
pip freeze --exclude-editable > requirements.txt
```

## Class Factories

This section is flask-app sepcific, but the principle applies everywhere.

This application is a flask micro-service, and does not need a "main" anywhere. Services like uwsgi and flask commandline expect to find a callable object in a module.

I created a module called flask\_app.py inside randomwebapp which creates a global app object using a class factory which lives inside another module create\_app.py.

Hence the module we want to define in uwsgi.ini becomes randomwebapp.flask\_app.

```ini
module = randomweb_app.flask_app
callable = app
```

The class factory function create\_app.create\_app does flask initializaiton based on the passed configuration. This is now the only user object we want to expose in my package's namespace, as it will be useful in testing.


## Test cases and code coverage

With distributed packages, there are a few options for testing. We cannot rely on test-discovery, as we want my tests to be deployable.

We can exploit the \_\_init\_\_.py again to bring all test classes directly into the namespace of the test package.

```python
from .tests_bettermathlib import BetterMathTestCases
```

Now unittests can be run via the unittest module. We can choose to run both the test packages together or seperately.

```bash
python -m unittest randomwebapp_tests bettermathlib_tests
```

For Flask we can use a flask command-line-interface property to explicitly define all the test packages that verify this application.

```python
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    testmodules = [
        'bettermathlib_tests',
        'randomwebapp_tests',
    ]
    suite = unittest.TestSuite()
    for t in testmodules:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))
    unittest.TextTestRunner(verbosity=2).run(suite)
```

Now flask tests starts working for me -

```bash
(venv) ...>flask test
test_better_random (bettermathlib_tests.tests_bettermathlib.BetterMathTestCases) ... ok
test_app_exists (randomwebapp_tests.tests_basic.BasicsTestCase) ... ok
test_app_is_testing (randomwebapp_tests.tests_basic.BasicsTestCase) ... ok
test_home_page (randomwebapp_tests.tests_client.FlaskClientTestCase) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.036s

OK
```

and code coverage

```bash
coverage run -m flask test
coverage report
```

## DockerFiles

There are two DockerFiles one for production and one for unit-testing.
The production docker files installs the packages non-editable.

```bash
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install  --no-deps bettermath-lib/
RUN python3 -m pip install  --no-deps randomweb-app/
```

The unittest takes the production docker image and uninstalls the two packages and re-installs them editable.
This allows us to retrieve code-coverage results from a container execution.

```bash
RUN python3 -m pip uninstall -y bettermath-lib
RUN python3 -m pip uninstall -y randomweb-app
RUN python3 -m pip install  coverage
RUN python3 -m pip install  --no-deps -e bettermath-lib/
RUN python3 -m pip install  --no-deps -e randomweb-app/
```
