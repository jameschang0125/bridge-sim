#include "dll.h"
#include "portab.h"
#include "gen.hpp"
#include <iostream>

int main(){
    SetMaxThreads(32);
    std::string resp("/tmp2/jameschang/bridge/res");
    std::string dealp("/tmp2/jameschang/bridge/deal");
    std::string seed = resp + dealp + "this1sacuterandomseedouowo";
    
    HandGenerator HG(seed);
    HG.fullgen(resp, dealp, 1000, 1);
}
