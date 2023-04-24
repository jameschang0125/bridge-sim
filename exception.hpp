#pragma once
#include <exception>


const std::string LeadErrorMsg("[ERROR] ");

class ExceptionMsg: public std::exception
{
public:
    explicit ExceptionMsg(const char* msg): msg(LeadErrorMsg + msg) {}
    explicit ExceptionMsg(std::string &msg): msg(LeadErrorMsg + msg) {}
    virtual char const* what() const noexcept {return msg.c_str();}
protected:
    std::string msg;
};