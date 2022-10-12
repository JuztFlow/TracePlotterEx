# TracePlotter
An open alternative to PingPlotter but with way more data!

What makes this different?
```
                (10.1.1.1, 100%)
                (localhost     )
                (Hop 1, RTT 0.2)
                       |
                      ___
                     |   |
(10.2.1.1, 75%  )____.   .____(10.3.1.1, 25%  )
(2.ibone.local. )             (1.ibone.local. ) <--- Click for ping RTT and related node trace data.
(Hop 2, RTT 15.0)             (Hop 2, RTT 24.0)      you can so choose to extend known hosts that have
        |                             |              used this node in the past for previous traces.
        |                             |              this allows for visual real time backbone monitoring.
        ._____________________________.
                        |
                        |
                 (10.4.1.1, 100% )
                 (mysite.local.  )
                 (Hop 3, RTT 21.0)   
```                
The plotter API allows for router level resolution. Each hop is traced out displaying frequency of router usage as a percentage, round trip time in milliseconds, and if available DNS resolution. Further resolution can be achieved by clicking on a node which will display the full router history including dropped packets and statistical RTT ping data. As stated above, you can also build out additional connected nodes to a separate host simultaneously!

More info to come...

Thanks,

Alex Libby
