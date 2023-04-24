#pragma once
#include "dll.h"
#include "portab.h"
#include <iostream>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>
#include <random>
#include <bitset>
#include <ctime>
#include <utility>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <typeinfo>
#include "exception.hpp"
#define ll long long
#define ull unsigned long long
#define pss std::pair<short, short>
#define s second
#define f first
#define N_deck 52
#define N_suit 13
#define N_maxDDTables 32 // when all trump filters
/*
MAXNOOFTABLES 40
DDS_STRAINS 5
*/

class Hasher{
public:
    Hasher(const std::string sd);
    ~Hasher();
    ull hash();
private:
    std::seed_seq seq;
};

class HandGenerator{
public:
    HandGenerator(const std::string sd);
    ~HandGenerator();
    void gen(ddTableDeals &deals, ddTablesRes &res);
    void refresh();
    void fullgen(std::string &resp, std::string &dealp, int T = 1000, int showEvery = -1);
private:
    int trumpfilter[5];     // {0}: calc res for all trump
	std::mt19937_64 randgen;
    Hasher hasher;
    pss arr[N_deck];        // use to shuffle
};
