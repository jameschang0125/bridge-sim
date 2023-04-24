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

    /* DEBUG
    std::cerr << "[DEBUG]\n";
    for(int k = 0; k < deals.noOfTables; k++){
        for(int i = 0; i < 4; i++){
            for(int j = 0; j < 4; j++){
                std::cerr << std::bitset<16>(deals.deals[k].cards[i][j]) << " ";
            }
            std::cerr << std::endl;
        }
    }
    std::cerr << std::endl; */

    CalcAllTables(&deals, -1, trumpfilter, &res, (allParResults*)0);
}

void HandGenerator::fullgen(std::string &resp, std::string &dealp, int T, int showEvery){
    constexpr int batch = 32;
    constexpr int rr = 1000; // refresh every 1000 deals
    if(showEvery < 0) showEvery = rr;
    
    ddTableDeals TD; 
    ddTablesRes TR;
    TD.noOfTables = batch;
    int fd_deal = open(dealp.c_str(), O_RDWR | O_CREAT, S_IRWXU);
    int fd_res = open(resp.c_str(), O_RDWR | O_CREAT, S_IRWXU);

    std::cout << "--- generating deals and results ---" << std::endl;
    for(int i = 0, tmp; i < T; i += batch){
        gen(TD, TR);
        if(i % rr < batch) refresh();
        if(i % showEvery < batch) std::cout << i << std::endl;
        for(int j = 0; j < batch; j++){
            if((tmp = write(fd_deal, &(TD.deals[j]), sizeof(ddTableDeal))) < sizeof(ddTableDeal)){
                std::cerr << "[ERROR] write to " << dealp << " failed, " << tmp << "/" << sizeof(ddTableDeal) << std::endl;
                exit(1);
            }
            if((tmp = write(fd_res, &(TR.results[j]), sizeof(ddTableResults))) < sizeof(ddTableResults)){
                std::cerr << "[ERROR] write to " << dealp << " failed, " << tmp << "/" << sizeof(ddTableResults) << std::endl;
                exit(1);
            }
        } 
    }
    close(fd_deal), close(fd_res);
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


