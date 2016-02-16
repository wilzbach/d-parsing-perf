#include <stdio.h>
#include <iostream>
#include <fstream>

int main (int argc, char* argv[])
{
    if( argc <= 1){
        printf("<file>");
        return 0;
    }
    FILE* myfile = fopen(argv[1], "r");
    int cases = 0, nr_items = 0;
    if (fscanf(myfile, "%d %d", &cases, &nr_items) == 0)
    {
        printf("invalid header");
    }
    long counter = 0;
    for(int i=0; i< cases; ++i)
    {
        int* k = new int[nr_items];
        for(int j=0; j < nr_items; ++j){
            fscanf(myfile, "%d", &k[j]);
        }
        for(int j=0; j < nr_items; ++j){
            counter += k[j];
        }

    }
    std::cout << counter << "\n";
    return 0;
}
