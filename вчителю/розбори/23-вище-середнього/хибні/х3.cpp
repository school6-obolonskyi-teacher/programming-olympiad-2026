// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    long long sum = 0;
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        sum += a[i];
    }
    long long avg = llround((double)sum / n);
    int cnt = 0;
    for (int i = 0; i < n; i++)
        if (a[i] > avg)
            cnt++;
    cout << cnt << endl;
    return 0;
}
