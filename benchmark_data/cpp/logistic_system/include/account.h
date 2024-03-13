#ifndef ACCOUNT_H
#define ACCOUNT_H

#include <stdio.h>
#include <string>
#include <vector>
#include <iostream>
using namespace std;

enum authority { root, admin, user };

struct AccountNode {
    string id;
    string password;
    string name;
    string phone;
    double money;
    string address;
    authority type;
    AccountNode();
    AccountNode(
        string _id,
        string _pwd,
        string _nm,
        string _ph,
        double _m,
        string _ad,
        authority _t = authority::user
    );
    friend ostream& operator<<(ostream& out, AccountNode& a);
};

#endif