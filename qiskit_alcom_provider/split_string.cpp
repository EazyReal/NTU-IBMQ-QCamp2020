#include <sstream>
#include <cstdio>
#include <string>
#include <iostream>
#include <vector>

using namespace std;

vector<string> split(string s, char delimiter='\n') {
    vector<string> ret;
    size_t n = 0;
    auto it = s.begin(), end = s.end(), first = s.begin();
    for (first = it; it != end; ++it) {
        if (delimiter == *it) {
            ret.push_back(string(first, it));
            ++n;
            first = ++it;
        }
    }
    return ret;
}


signed main()
{
    string qasm = "OPENQASM 2.0;include 'qelib1.inc';\nqreg q[3];\ncreg c[3];\nh q[0];\ncx q[0],q[1];\ncx q[1],q[2];\nmeasure q[0] -> c[0];\nmeasure q[1] -> c[1];\nmeasure q[2] -> c[2];";
    stringstream s1(qasm);
    vector<string> lines = split(qasm, '\n');
    for(auto& line : lines)
    {
        cout << line << endl;
    }
    return 0;
}