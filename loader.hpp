#pragma once
#include "dll.h"
#include "portab.h"
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <typeinfo>
#include <utility>
#include <string>
#include "exception.hpp"
#define ll long long
#define ull unsigned long long
#define pdd std::pair<ddTableDeal, ddTableResults>

/*
T load[1](*, [2])

[1]: [<empty>|Deal|Res]
    - <empty>: Load both deal and result.
    - Deal: load deal only
    - Res: load result only
[2]: [<empty>|id]
    - <empty>: sequential access
    - id: Access a specific deal. Not very recommended.
*  : optional, see below

Calling different options might cause unexpected behavior. To do so, create multiple DataManager.
If T == int, return == 0 iff on success. 
If T != int, an exception is thrown.
*/

class DataManager{
public:
    DataManager(const std::string &dealp = "", const std::string &resp = "");
    ~DataManager() {};
    int load(ddTableDeal &deal, ddTableResults &res, ull id);
    int load(ddTableDeal &deal, ddTableResults &res);
    int loadDeal(ddTableDeal &deal, ull id);
    int loadDeal(ddTableDeal &deal);
    int loadRes(ddTableResults &res, ull id);
    int loadRes(ddTableResults &res);
    pdd load(ull id);
    pdd load();
    ddTableDeal loadDeal(ull id);
    ddTableDeal loadDeal();
    ddTableResults loadRes(ull id);
    ddTableResults loadRes();

    // TODO: maybe use template

private:
    FILE *fdeal, *fres;
};
