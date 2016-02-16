#!/usr/bin/env rdmd

import std.stdio; // File
import std.array;
import std.algorithm;
import std.conv; // to

void main(string[] args)
{
    if(args.length == 1){
        writeln("No args");
        return;
    }
    auto file = new File(args[1], "r");
    int nr_tests, nr_tests_per_line;
    file.readf("%d %d\n", &nr_tests, &nr_tests_per_line);
    long counter = 0;
    foreach(i; 0..nr_tests){
        auto nrs = file.readln.splitter.map!(to!int).array;
        counter += nrs.sum;
    }
    writeln(counter);
}
