import std.stdio;
import std.array;
import std.mmfile;
import std.string;
import std.algorithm;
import std.conv;

void main(string[] args)
{
    if(args.length == 1){   
        writeln("No args");
        return;
    }
    auto mmFile = new MmFile(args[1]);
    
    // read header
    auto file = splitter(cast(string)mmFile[0..mmFile.length], '\n');
    auto p = splitter(file.front, ' ').map!(to!int);
    file.popFront();

    long counter = 0;

    foreach(line; file){
        auto csv = splitter(line, ' ').map!(to!int).array;
        if(csv.length > 0){
            counter += csv.sum;
        }
    }
    writeln(counter);
}
