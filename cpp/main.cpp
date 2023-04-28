#include "dll.h"
#include "portab.h"
#include "gen.hpp"
#include "loader.hpp"
#include "util.hpp"
#include <iostream>

int main(){
    SetMaxThreads(80);
    std::string dealp("../data/deal");
    std::string resp("../data/res");
    std::string seed = resp + dealp + "this1sacuterandomseedouowo";
    
    HandGenerator HG(seed);
    HG.fullgen(resp, dealp, 100000);
}
