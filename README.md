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

Quick benchmark on a Raspberry-pi 2 with wrk2
=============================================

```
alex@asus  ~  wrk -t2 -d30s -R600 -L http://rpi2:8000/json
Running 30s test @ http://rpi2:8000/json
  2 threads and 10 connections
  Thread calibration: mean lat.: 2550.746ms, rate sampling interval: 7540ms
  Thread calibration: mean lat.: 2496.937ms, rate sampling interval: 7294ms
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     7.44s     1.99s   12.15s    63.20%
    Req/Sec   202.00     10.42   215.00     50.00%
  Latency Distribution (HdrHistogram - Recorded Latency)
 50.000%    7.37s 
 75.000%    9.00s 
 90.000%   10.05s 
 99.000%   11.62s 
 99.900%   12.12s 
 99.990%   12.16s 
 99.999%   12.16s 
100.000%   12.16s 

  Detailed Percentile spectrum:
       Value   Percentile   TotalCount 1/(1-Percentile)

    3624.959     0.000000            1         1.00
    4726.783     0.100000          829         1.11
    5443.583     0.200000         1649         1.25
    6152.191     0.300000         2473         1.43
    6795.263     0.400000         3293         1.67
    7368.703     0.500000         4112         2.00
    7778.303     0.550000         4524         2.22
    8159.231     0.600000         4936         2.50
    8495.103     0.650000         5345         2.86
    8716.287     0.700000         5762         3.33
    9003.007     0.750000         6175         4.00
    9142.271     0.775000         6389         4.44
    9265.151     0.800000         6587         5.00
    9404.415     0.825000         6786         5.71
    9576.447     0.850000         6995         6.67
    9781.247     0.875000         7203         8.00
    9961.471     0.887500         7302         8.89
   10051.583     0.900000         7405        10.00
   10149.887     0.912500         7512        11.43
   10280.959     0.925000         7608        13.33
   10461.183     0.937500         7713        16.00
   10649.599     0.943750         7762        17.78
   10772.479     0.950000         7812        20.00
   10862.591     0.956250         7866        22.86
   10977.279     0.962500         7916        26.67
   11247.615     0.968750         7970        32.00
   11288.575     0.971875         7995        35.56
   11337.727     0.975000         8021        40.00
   11378.687     0.978125         8045        45.71
   11427.839     0.981250         8073        53.33
   11493.375     0.984375         8095        64.00
   11534.335     0.985938         8108        71.11
   11567.103     0.987500         8122        80.00
   11599.871     0.989062         8135        91.43
   11665.407     0.990625         8149       106.67
   11894.783     0.992188         8159       128.00
   11927.551     0.992969         8168       142.22
   11943.935     0.993750         8172       160.00
   11968.511     0.994531         8179       182.86
   11984.895     0.995313         8187       213.33
   12001.279     0.996094         8191       256.00
   12025.855     0.996484         8195       284.44
   12042.239     0.996875         8200       320.00
   12050.431     0.997266         8202       365.71
   12058.623     0.997656         8204       426.67
   12075.007     0.998047         8208       512.00
   12083.199     0.998242         8210       568.89
   12107.775     0.998437         8214       640.00
   12107.775     0.998633         8214       731.43
   12107.775     0.998828         8214       853.33
   12115.967     0.999023         8215      1024.00
   12124.159     0.999121         8217      1137.78
   12124.159     0.999219         8217      1280.00
   12132.351     0.999316         8218      1462.86
   12140.543     0.999414         8220      1706.67
   12140.543     0.999512         8220      2048.00
   12140.543     0.999561         8220      2275.56
   12140.543     0.999609         8220      2560.00
   12148.735     0.999658         8221      2925.71
   12148.735     0.999707         8221      3413.33
   12148.735     0.999756         8221      4096.00
   12156.927     0.999780         8223      4551.11
   12156.927     1.000000         8223          inf
#[Mean    =     7438.671, StdDeviation   =     1993.591]
#[Max     =    12148.736, Total count    =         8223]
#[Buckets =           27, SubBuckets     =         2048]
----------------------------------------------------------
  11721 requests in 30.00s, 74.59MB read
Requests/sec:    390.65
Transfer/sec:      2.49MB
```

    
### TODO

1. Tests.
2. Documentation.
3. Better benchmarking
