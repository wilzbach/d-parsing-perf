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
    scope(exit) file.close();
    int nr_tests = file.readln.chomp.to!int;
    long counter = 0;
    foreach(i; 0..nr_tests){
        int nr_vs = file.readln.chomp.to!int;
        counter += nr_vs;
    }
    writeln(counter);
}
