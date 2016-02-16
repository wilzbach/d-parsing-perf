#!/usr/bin/env rdmd

import std.stdio; // File
import std.string;
import std.conv; // to

void main(string[] args)
{
    if(args.length == 1){   
        writeln("No args");
        return;
    }
    auto file = new File(args[1], "r");
    int nr_tests;
    file.readf(" %d ", &nr_tests);
    long counter = 0;
    foreach(i; 0..nr_tests){
        int nr_vs;
        file.readf("%d\n", &nr_vs);
        counter += nr_vs;
    }
    writeln(counter);
}
