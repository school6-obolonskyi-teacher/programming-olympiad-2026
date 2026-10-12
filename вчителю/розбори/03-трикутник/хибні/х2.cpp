// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    int side[3];
    cin >> side[0] >> side[1] >> side[2];
    sort(side, side + 3);
    if (side[0] + side[1] > side[2])
        cout << "YES\n";
    else
        cout << "NO\n";
    return 0;
}
