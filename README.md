D Parsing performance guide
===========================

This guide will compare multiple variants of writing parser and give guidance.
Hence this information might be useful if you plan to parse a lot of data in D.

All guidances are backed by real test and code, which you can run yourself.
Tests are run with `gdc -O3`.

Index
------

- [How to parse a line that contains just one int](#readln-int)
- [How to parse a line that contains multiple int?](#readln-ints)

How to parse a line that contains just one int?
----------------------------------------------
<a name="readln-int"></a>

We have a line that contains just a number

```
5\n
```

Testset contains 100M lines.

### A) using `readf`

```
int nr;
file.readf("%d\n", &nr);
```

### B) using `readln.chomp.to!int`

```
int nr = file.readln.chomp.to!int;
```
This is takes 107% compared to A.

However when there is __unknown whitespace__ this method performs faster!

How to parse a line that contains multiple int?
----------------------------------------------
<a name="readln-ints"></a>

Testset: 10M lines with 100 numbers

### A) using `file.readln.split.map!(to!int)`

```
int[] nrs = file.readln.split.map!(to!int);
```

### B) using `file.readln.split.map!(to!int).array`

```
int[] nrs = file.readln.split.map!(to!int).array;
```

Prefer to work with ranges. However the runtime overhead to allocate and copy
the array is only slightly noticabale: 107%.

### C) using `readf`

```
int[] nrs = new int[](nr_tests_per_line);
foreach(j; 0..nr_tests_per_line){
    file.readf(" %d", &nrs[j]);
}
```

This method requires to know the array length __in advance__ and even takes 280% than A).


How to run the tests
--------------------


You will need `gdc` and python3.

### Running all tests

```
./run.py
```

### Running only a single test

```
./run.py readln_ints 
```
### Running only small tests

```
./run.py -s
```

For more info see `run.py --help``

How to add your own tests
---------------------

- create a new folder
- add your tests to `tests.json`
- add your results to the README.md and send a PR

License
-------

THE BEER-WARE LICENSE (Revision 42):
Greenify wrote this file.  As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.
