#include "dll.h"
#include "portab.h"
#include "gen.hpp"
#include "loader.hpp"
#include "util.hpp"
#include <iostream>

int main(){
    SetMaxThreads(32);
    std::string dealp("data/deal");
    std::string resp("data/res");
    std::string seed = resp + dealp + "this1sacuterandomseedouowo";
    
    HandGenerator HG(seed);
    HG.fullgen(resp, dealp, 100, 1);

    ddTableDeal deal;
    ddTableResults res, res2;
    DataManager DM(dealp, resp);
    DM.load(deal, res, 67);

    CalcDDtable(deal, &res2);
    for(int i = 0; i < 5; i++) for(int j = 0; j < 4; j++)
        if(res.resTable[i][j] != res2.resTable[i][j]) throw ExceptionMsg("results does not match!");
    std::cout << "Results matched!" << std::endl;

    HandViewer HV;
    HV.display(deal, res);
}
