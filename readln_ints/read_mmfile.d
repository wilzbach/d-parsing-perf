import std.stdio;
import std.array;
import std.mmfile;
import std.string;
import std.algorithm;
import std.conv;
import std.range;

auto popi(Range)(ref Range a){
    auto b = a.front;
    a.popFront();
    return b;
}

void main(string[] args)
{
    if(args.length == 1){   
        writeln("No args");
        return;
    }
    scope mmFile = new MmFile(args[1]);
    auto file = splitter(cast(string)mmFile[0..mmFile.length], '\n').filter!"!a.empty";
    
    // read header
    //auto p = file.popi.splitter(' ').map!(to!int).array;

    long counter = 0;
    writeln(file.takeOne.front);
    writeln(file);

    foreach(line; file){
        int[] csv = line.splitter(' ').map!(to!int).array;
        counter += csv.sum;
    }
    writeln(counter);
}
