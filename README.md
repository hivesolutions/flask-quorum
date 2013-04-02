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

## Build Automation

[![Build Status](https://travis-ci.org/hivesolutions/flask_quorum.png?branch=master)](https://travis-ci.org/hivesolutions/flask_quorum)
