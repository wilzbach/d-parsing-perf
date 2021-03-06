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
- `mmFile` is faster (it's cached in your RAM, so don't use it for enormous files)

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
auto file = splitter(cast(string)mmFile[0..mmFile.length], '\n').filter!"!a.empty";

// read header
auto p = splitter(file.front, ' ').map!(to!int).array;
file.popFront();

foreach(line; file){
    int[] csv = line.splitter(' ').map!(to!int).array;
    counter += csv.sum;
}
```

Using the memory yields the highest performance, however it's also a bit more
complex.

### B) using `splitter` and `map` 

```
int[] nrs = file.readln.splitter.map!(to!int);
```

__Recommended!__ (it's easier to remember)

### C) using `csvReader`

```
auto nrs = file.readln.csvReader!int(' ').front;
```

The csvReader can be useful if you want to serialize into a struct.

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
.read_mmfile 100.0% (2.8641 s)
.read_mmfile_async 114.8% (3.2872 s)
.splittermap 128.8% (3.6901 s)
.splittermap_async 129.2% (3.7001 s)
.splittermap_async_linewise 132.6% (3.7964 s)
.splittermap_array 164.8% (4.7198 s)
*.main11 179.7% (5.1480 s)
.main_vector 214.6% (6.1450 s)
.readcsv 219.4% (6.2851 s)
.splitmap_buffer 231.6% (6.6346 s)
.splitmap 242.7% (6.9510 s)
*.main_c 246.1% (7.0484 s)
.splitmap_array 246.9% (7.0716 s)
.readcsv_array 254.9% (7.3009 s)
.readcsv_all 352.4% (10.0941 s)
*.readfarr 587.8% (16.8339 s)
.main 781.5% (22.3829 s)

```

- `*` require prior knowledge of the length of numbers
- `async` variations convert are done via parallel map
  - they always convert their output to arrays
  - they are better ways to do this


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
