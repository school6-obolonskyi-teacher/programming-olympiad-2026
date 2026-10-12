// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++)
        cin >> a[i];
    for (int i = 0; i < n; i++) {
        bool smallest = true;
        for (int j = 0; j < n; j++) {
            if (a[j] < a[i]) {
                smallest = false;
                break;
            }
        }
        if (smallest) {
            cout << a[i] << '\n';
            return 0;
        }
    }
    return 0;
}
