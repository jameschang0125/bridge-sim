#include "loader.hpp"

DataManager::DataManager(const std::string &dealp, const std::string &resp):
    fdeal{dealp.empty() ? nullptr : fopen(dealp.c_str(), "r")}, 
    fres{resp.empty() ? nullptr : fopen(resp.c_str(), "r")}
{}

int DataManager::load(ddTableDeal &deal, ddTableResults &res){
    return loadDeal(deal) + loadRes(res);
}

int DataManager::load(ddTableDeal &deal, ddTableResults &res, ull id){
    return loadDeal(deal, id) + loadRes(res, id);
}

int DataManager::loadDeal(ddTableDeal &deal){
    return fread(&deal, sizeof(ddTableDeal), 1, fdeal) == 1 ? 0 : -1;
}

int DataManager::loadDeal(ddTableDeal &deal, ull id){
    fseek(fdeal, id * sizeof(ddTableDeal), SEEK_SET);
    return loadDeal(deal);
}

int DataManager::loadRes(ddTableResults &res){
    return fread(&res, sizeof(ddTableResults), 1, fres) == 1 ? 0 : -1;
}

int DataManager::loadRes(ddTableResults &res, ull id){
    fseek(fres, id * sizeof(ddTableResults), SEEK_SET);
    return loadRes(res);
}

pdd DataManager::load(){
    return std::make_pair(loadDeal(), loadRes());
}

pdd DataManager::load(ull id){
    return std::make_pair(loadDeal(id), loadRes(id));
}

ddTableDeal DataManager::loadDeal(){
    ddTableDeal deal;
    if(loadDeal(deal)) throw ExceptionMsg("load deal failed");
    return deal;
}

ddTableDeal DataManager::loadDeal(ull id){
    ddTableDeal deal;
    if(loadDeal(deal, id)) throw ExceptionMsg("load deal failed");
    return deal;
}

ddTableResults DataManager::loadRes(){
    ddTableResults res;
    if(loadRes(res)) throw ExceptionMsg("load res failed");
    return res;
}

ddTableResults DataManager::loadRes(ull id){
    ddTableResults res;
    if(loadRes(res, id)) throw ExceptionMsg("load res failed");
    return res;
}