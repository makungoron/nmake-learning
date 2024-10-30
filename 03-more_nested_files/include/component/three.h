#pragma once
#include "component/base.h"

class SubClass : MyClass {
public:
    int z;
    int sum() const;
    SubClass(int x = 0, int y = 0, int z = 0) : MyClass(x, y), z(z) {}
};
