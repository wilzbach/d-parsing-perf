#include <stdio.h>
#include <iostream>
#include <fstream>

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
    for(int i=0; i< cases; ++i)
    {
        int* k = new int[nr_items];
        for(int j=0; j < nr_items; ++j){
            myfile >> k[j]; 
        }
        for(int j=0; j < nr_items; ++j){
            counter += k[j];
        }

    }
    std::cout << counter << "\n";
    return 0;
}
