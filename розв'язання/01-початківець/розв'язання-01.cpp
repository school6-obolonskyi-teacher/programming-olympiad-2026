// Завдання 1: Сума цифр
// Складність: O(log n) час, O(1) пам'ять
// Гімназія №6, м. Дніпро

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    long long n;
    cin >> n;
    
    int sum = 0;
    while (n > 0) {
        sum += n % 10;
        n /= 10;
    }
    
    cout << sum << endl;
    return 0;
}
