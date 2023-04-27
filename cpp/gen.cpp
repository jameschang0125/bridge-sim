#include "gen.hpp"

HandGenerator::HandGenerator(const std::string sd):
    trumpfilter{0, 0, 0, 0, 0}, randgen{(long unsigned int)time(0)}, hasher{sd}
{
    for(int i = 0, t = 0; i < 4; i++){
        for(int j = 2; j <= 14; j++, t++){
            arr[t] = std::make_pair(i, 1 << j);
        }
    }
}

HandGenerator::~HandGenerator() {}

void HandGenerator::gen(ddTableDeals &deals, ddTablesRes &res){
    // generate deals
    for(int k = 0; k < deals.noOfTables; k++){
        std::shuffle(arr, arr + N_deck, randgen);
        for(int i = 0; i < 4; i++) for(int j = 0; j < 4; j++) deals.deals[k].cards[i][j] = 0;
        
        for(int i = 0; i < 4; i++){
            for(int j = 13 * i; j < 13 * (i + 1); j++)
                deals.deals[k].cards[i][arr[j].f] |= arr[j].s;
        }
    }

    CalcAllTables(&deals, -1, trumpfilter, &res, (allParResults*)0);
}

void HandGenerator::fullgen(std::string &resp, std::string &dealp, int T, int showEvery){
    constexpr int batch = 32;
    constexpr int rr = 10000; // refresh every 10000 deals
    if(showEvery < 0) showEvery = rr;
    
    ddTableDeals TD; 
    ddTablesRes TR;
    TD.noOfTables = batch;
    FILE* fdeal = fopen(dealp.c_str(), "w");
    FILE* fres = fopen(resp.c_str(), "w");
    
    if(fdeal == nullptr) throw ExceptionMsg("can't open deal file");
    if(fres == nullptr) throw ExceptionMsg("can't open res file");

    std::cout << "--- generating deals and results ---" << std::endl;
    for(int i = 0, tmp; i < T; i += batch){
        gen(TD, TR);
        if(i % rr < batch) refresh();
        if(i % showEvery < batch) std::cout << i << std::endl;
        if((tmp = fwrite(TD.deals, sizeof(ddTableDeal), batch, fdeal)) != batch)
            throw ExceptionMsg("write deal failed");
        if((tmp = fwrite(TR.results, sizeof(ddTableResults), batch, fres)) != batch)
            throw ExceptionMsg("write res failed");
    }
    fclose(fdeal), fclose(fres);
    std::cout << "--- finished ---" << std::endl;
}

void HandGenerator::refresh(){
    randgen = std::mt19937_64(hasher.hash());
}

Hasher::Hasher(const std::string sd):
    seq(sd.begin(), sd.end())
{}  

Hasher::~Hasher() {}

ull Hasher::hash(){
    unsigned tmp[2];
    seq.generate(tmp, tmp + 2);
    return ((ull)tmp[0] << 32) + (ull)tmp[1] + time(0);
}


