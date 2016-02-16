#!/usr/bin/env rdmd

import std.stdio; // File
import std.conv;
import std.random;
import std.range;
import std.algorithm;

void main(string[] args)
{
    if(args.length < 3){
        writeln("<file> <nr> <per-line>");
        return;
    }
    auto file = new File(args[1], "w");
    int nr_tests = args[2].to!int;
    int nr_tests_per_line = args[3].to!int;
    file.writefln("%d %d", nr_tests, nr_tests_per_line);
    foreach(i; 0..nr_tests){
        auto nrs = generate!(()=>uniform(0,100)).take(nr_tests_per_line).map!(to!string);
        file.writeln(nrs.joiner(" "));
    }
}
