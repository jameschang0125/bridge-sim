#include "util.hpp"

const std::string hand{"NESW"}, card{"--23456789TJQKA"}, suit{"SHDCN"};

void HandViewer::display(ddTableDeal &deal, ddTableResults &res){
    display(deal); display(res);
}

void HandViewer::display(ddTableDeal &deal){
    std::cout << "--- display deal ---" << std::endl;
    for(int i = 0; i < 4; i++){
        std::cout << hand[i] << std::endl;
        for(int j = 0; j < 4; j++){
            if(deal.cards[i][j] == 0) std::cout << '-';
            else for(int k = 14; k >= 2; k--) if(deal.cards[i][j] & (1 << k)) std::cout << card[k];
            std::cout << std::endl;
        }
        if(i < 3) std::cout << std::endl;
    }
    std::cout << "--------------------" << std::endl;
}

void HandViewer::display(ddTableResults &res){
    std::cout << "--- display result ---" << std::endl << '\t';
    for(int i = 0; i < 5; i++) std::cout << suit[i] << '\t';
    std::cout << std::endl;
    for(int i = 0; i < 4; i++){
        std::cout << hand[i] << '\t';
        for(int j = 0; j < 5; j++) std::cout << res.resTable[j][i] << '\t';
        std::cout << std::endl;
    }
    std::cout << "----------------------" << std::endl;
}

void HandViewer::rotate(ddTableDeal &deal, ddTableResults &res){
    rotate(deal); rotate(res);
}

void HandViewer::rotate(ddTableDeal &deal){
    // TODO
}

void HandViewer::rotate(ddTableResults &res){
    // TODO
}
