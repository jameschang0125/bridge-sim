#pragma once
#include "dll.h"
#include "portab.h"
#include <iostream>

class HandViewer{
public:
    HandViewer() {};
    ~HandViewer() {};
    void display(ddTableDeal &deal);
    void display(ddTableResults &res);
    void display(ddTableDeal &deal, ddTableResults &res);
    void rotate(ddTableDeal &deal);
    void rotate(ddTableResults &res);
    void rotate(ddTableDeal &deal, ddTableResults &res);
};

