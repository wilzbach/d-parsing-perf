#!/usr/bin/env rdmd

import std.stdio; // File
import std.string; // chomp
import std.conv;
import std.random;

void main(string[] args)
{
    if(args.length < 2){   
        writeln("<file> <nr>");
        return;
    }
    auto file = new File(args[1], "w");
    scope(exit) file.close();
    int nr_tests = args[2].to!int;
    file.writeln(nr_tests);
    foreach(i; 0..nr_tests){
        file.writeln(uniform(0,100));
    }
}
