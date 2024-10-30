#pragma once
#include <iostream>

class MyClass {
public:
    int x;
    int y;

    int sum() const;

    MyClass(int x = 0, int y = 0) : x(x), y(y) {}
};
