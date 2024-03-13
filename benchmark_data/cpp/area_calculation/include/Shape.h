#ifndef SHAPE_H
#define SHAPE_H

#include <stdlib.h>
#include <iostream>

class Shape {
 public:
    Shape();
    ~Shape();
    virtual double calcArea();
};



#endif