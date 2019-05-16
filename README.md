# StatDescriptor
StatDescriptor is an algorithm that finds descriptions of permutation statistics using mesh patterns.

StatDescriptor uses the library [permuta][1]. Before using StatDescriptor, permuta must be installed.

The *stats* folder contains an assortment of statistics found on [findstat.org][2], for which the algorithm can provide descriptions.

To run:
```
python stat_descriptor.py n₁ n₂ … nₖ
```
where n₁, n₂, … , nₖ are the numbers of the desired statistics from the *stats* folder.


This repository also includes a few additional things, such as a method to find the classical basis of a given set of permutations in `classical_basis.py` and a method to find the number of occurrences of a given mesh pattern in all permutations up to a given length in `find_stats.py`.

[1]: https://github.com/PermutaTriangle/Permuta
[2]: http://www.findstat.org/StatisticsDatabase
