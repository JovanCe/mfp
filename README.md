# mfp

This is a set of Python implementations of common maxflow algorithms together with the mechanism for generating flow network test problems using [Netgen C library](https://lemon.cs.elte.hu/trac/lemon/browser/lemon-benchmark/generators/netgen/netgen.c?rev=7). 

Netgen outputs graphs in [DIMACS format](http://prolland.free.fr/works/research/dsat/dimacs.html) so mirroring that, a dictionary representation is used to represent flow networks. Each arc is represented by a dictionary entry with the key being a tuple of connecting nodes while the value is the capacity of the arc.

The following algorithms are implemented:
* Ford-Fulkerson (with Dijkstra's shortest path)
* Edmonds-Karp
* Capacity scaling
* Generic push relabel
* Relabel to front
