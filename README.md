D Parsing performance guide
===========================

This guide will compare multiple variants of writing parser and give guidance.
Hence this information might be useful if you plan to parse a lot of data in D.

All guidances are backed by real test and code, which you can run yourself.
Tests are run with `ldc -O3 -release`.

Index
------

- [1) General rules](#general)
- [2) How to parse a line that contains just one int](#readln-int)
- [3) How to parse a line that contains multiple int?](#readln-ints)

1) General rules?
-----------------
<a name="general"></a>

- use `splitter` (`std.algorithm.iterator`) instead of `split` (it's lazy!)

2) How to parse a line that contains just one int?
--------------------------------------------------
<a name="readln-int"></a>

We have a line that contains just a number

```
5\n
```

Testset: 100M lines (~240M)

### A) using `readf`

```
int nr;
file.readf("%d\n", &nr);
```

### B) using `readln.chomp.to!int`

```
int nr = file.readln.chomp.to!int;
```
This is takes 106.1% compared to A.

However when there is __unknown whitespace__ this method performs faster!

### Comparison with Python

~ 318%

3) How to parse a line that contains multiple int?
-------------------------------------------------
<a name="readln-ints"></a>

We have a line that contains multiple numbers

```
5 3 5 6 9 100\n
```

Testset: 10M lines with 100 numbers (~2.8G)

### A) using `mmFile`

```
scope mmFile = new MmFile(args[1]);

// read header
auto file = splitter(cast(string)mmFile[0..mmFile.length], '\n');
auto p = splitter(file.front, ' ').map!(to!int);
file.popFront();

foreach(line; file){
    scope csv = splitter(line, ' ').map!(to!int).array;
    if(csv.length > 0){
            counter += csv.sum;
        }
    }
```

Using the memory yields the highest performance, however it's also a bit more
complex.

### B) using `splitter` and `map` 

```
int[] nrs = file.readln.splitter.map!(to!int);
```

### C) using `csvReader`

```
auto nrs = file.readln.csvReader!int(' ').front;
```

This is the fastest if you don't need to work on the array. For working on the
array `map` is faster!

__Don't__ use `file.byLine.joiner("\n").csvReader!int(' ')` - it is more expensive!

### D) using `readf`

```
int[] nrs = new int[](nr_tests_per_line);
foreach(j; 0..nr_tests_per_line){
    file.readf(" %d", &nrs[j]);
}
```

__Don't__ use something like this. It's very slow (2-3x!) and inflexible.


### Comparison with Python and C++

A lot of methods were tested - as you can see MMFile and `splitter` perform extremely well.
In fact even better than a normal C (`main_c`) or C++ (`main11`) implementation.

```
.read_mmfile 100.0% (2.8312 s)
.splittermap 135.9% (3.8489 s)
.splittermap_array 163.2% (4.6207 s)
*.main11 177.6% (5.0274 s)
.readcsv 215.5% (6.1004 s)
.main_vector 217.1% (6.1468 s)
*.main_c 223.8% (6.3353 s)
.splitmap_array 243.6% (6.8962 s)
.splitmap 245.4% (6.9483 s)
.splitmap_buffer 246.6% (6.9813 s)
.readcsv_array 256.4% (7.2589 s)
.readcsv_all 343.7% (9.7305 s)
*.readfarr 608.5% (17.2269 s)
.main 773.8% (21.9069 s)
```

`*` require prior knowledge of the length of numbers

How to run the tests
--------------------


You will need `gdc`, `rdmd` and python3.

### Running all tests

```
./run.py
```

### Running only a single test

```
./run.py readln_ints 
```
### Running only small tests

Running the large tests might take quite some time, hence to test or develop you
can use the `-s/--small` flag:

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
