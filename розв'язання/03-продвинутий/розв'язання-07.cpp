// Завдання 7: Послідовність Фібоначчі
// Складність: O(n) час, O(1) пам'ять
// Гімназія №6, м. Дніпро

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n;
    cin >> n;
    
    long long a = 0, b = 1;
    
    for (int i = 0; i < n; i++) {
        cout << a;
        if (i < n - 1) cout << " ";
        
        long long temp = a + b;
        a = b;
        b = temp;
    }
    cout << "\n";
    
    return 0;
}
