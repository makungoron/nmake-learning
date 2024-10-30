#include "lib.h"
#include "tool/calc.h"
#include "tool/common/common_tool.h"
#include "component/base.h"
#include "component/three.h"

int main() {
    hello(); // lib.h
    std::cout << add(1, 10) << std::endl; // tool/calc.cpp
    hello_world(); // tool/common/common_tool.cpp
    MyClass mc = {1, 2}; // component/base.cpp
    std::cout << mc.sum() << std::endl;
    SubClass sc = {1, 2, 3}; // component/three.cpp
    std::cout << sc.sum() << std::endl;
    return 0;
}
