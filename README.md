## Milvago

### Simplified Falcon web API with a built-in template engine.

WIP, technically started working on it in total of 4 hours ago. Why? It branched out of a personal project, mainly for productivity purposes.

```
 Milvago
    - A genus of bird of prey in the family Falconidae.
                 .------._
           .-````-.<')    `-.___
          (.----. _             '---.__.-
              __---'
            .---'``
             `""'-,
                   ````
```

This is a simplified interface for the falcon web framework with a built-in
support for jinja2 templates: The same performance without the boilerplate
code.



### The most simple of examples, let's call it uber_simple.py



```
from milvago import expose_web, Milvago


@expose_web('/')
def index(web):
    return 'Hello Milvago!'


milvago = Milvago([index()], debug=True)
server = milvago()
```

You can start the server by running `$ python uber_simple.py`
The example above will run the application in development mode
through wsgiref. If you want to run it in production, you should

1. Change

    `milvago = Milvago([index()], debug=True)`
    
    to
    
    `milvago = Milvago([index()], debug=False)`
    
2. Run it with gunicorn:
    gunicorn uber_simple:server

### Benchmarking

An identical application has been set in several common python
web-frameworks(can be found in the [_benchmarks](https://github.com/axegon/Milvago/tree/master/_benchmarks) directory)
and tested in identical scenarios. Each framework has been
tested with wrk2, 6 times.

The scores bellow are averaged of all 6 tests:

Running 30s tests, 4 threads and 10 connections:


| Flask                 | Milvago                | Cherrypy              | Hug                    | fastapi               | Tornado               |
|-----------------------|------------------------|-----------------------|------------------------|-----------------------|-----------------------|
| 14362 requests        | 23662 requests         | 19874 requests        | 19182 requests         | 21123 requests        | 19801 requests        |
| 1.81GB read           | 2.98GB read            | 2.50GB read           | 2.82GB read            | 2.66GB read           | 2.49GB read           |
| Requests/sec: 478.58  | Requests/sec: 788.65   | Requests/sec: 662.26  | Requests/sec: 639.22   | Requests/sec: 703.96  | Requests/sec: 659.90  |
| Transfer/sec: 61.64MB | Transfer/sec: 101.58MB | Transfer/sec: 85.28MB | Transfer/sec:  96.36MB | Transfer/sec: 90.65MB | Transfer/sec: 85.01MB |





    
### TODO

1. Tests.
2. Documentation.
