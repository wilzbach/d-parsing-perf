#include <stdio.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <iterator>

int main (int argc, char* argv[])
{
    if( argc <= 1){
        printf("<file>");
        return 0;
    }
    std::ifstream myfile(argv[1]);
    int cases = 0, nr_items = 0;
    myfile >> cases >> nr_items;
    long counter = 0;
    std::string line;
    while ( getline(myfile, line) ) {
        std::istringstream is(line);
        auto vs = std::vector<int> (std::istream_iterator<int>(is),std::istream_iterator<int>());
        for(auto n: vs) 
            counter += n;
    }
    std::cout << counter << "\n";
    return 0;
}
