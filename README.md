# [![Quorum Extensions for Flask](res/logo.png)](http://flask-quorum.hive.pt)

A small extension framework for Flask to easy a series of simple tasks.

## Usage

```python
import flask
import quorum

app = quorum.load(
    name = __name__
)

@app.route("/", methods = ("GET",))
def index():
    return flask.render_template("index.html.tpl")

if __name__ == "__main__":
    quorum.run()
```

Creation of background callables, that will execute every one second in a separate thread

```python
@quorum.background(timeout = 1.0)
def hello_recursive():
    print("hello word")
```

## Building

```bash
sphinx-build -b html doc doc/_build
```

## Documentation

Extra documentation is available under our readthedocs.com [page](https://quorum.readthedocs.org). Keep
in mind that some delay may exist between the current repository `master` version and the documentation.

We need people to help documentation the code base if you know anyone please contact us.

## License

Quorum Extensions for Flask is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://github.com/hivesolutions/flask-quorum/workflows/Main%20Workflow/badge.svg)](https://github.com/hivesolutions/flask-quorum/actions)
[![PyPi Status](https://img.shields.io/pypi/v/quorum.svg)](https://pypi.python.org/pypi/quorum)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
