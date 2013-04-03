# Quorum Extensions for Flask

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

Creation of background callbables, that will execute every one second in a separate thread

```python
@quorum.background(timeout = 1.0)
def hello_recursive():
    print "hello word"
```

## Building

    sphinx-build -b html doc doc/_build
    
## Documentation

Extra documentation is available under our readthedocs.com [page](https://quorum.readthedocs.org). Keep
in mind that some delay may exist between the current repository `master` version and the documentation.

We need people to help documentation the code base if you know anyone please contact us.

## Build Automation

[![Build Status](https://travis-ci.org/hivesolutions/flask_quorum.png?branch=master)](https://travis-ci.org/hivesolutions/flask_quorum)
