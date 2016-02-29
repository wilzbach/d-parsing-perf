import std.stdio;
import std.array;
import std.mmfile;
import std.string;
import std.algorithm;
import std.conv;
import std.range;
import std.parallelism;

void main(string[] args)
{
    if(args.length == 1){   
        writeln("No args");
        return;
    }
    scope mmFile = new MmFile(args[1]);

    auto file = splitter(cast(string)mmFile[0..mmFile.length], '\n').filter!"!a.empty";
    file.popFront;
    auto lines = file.map!(a => a.splitter(' ').map!(to!int).array);
    
    // read header
    //auto p = file.popi.splitter(' ').map!(to!int).array;

    long counter = 0;
    //writeln(file.takeOne.front);
    //writeln(file);

    auto asyncReader = taskPool.asyncBuf(lines);
    foreach(nrs; asyncReader){
        counter += nrs.sum;
    }
    writeln(counter);
}
