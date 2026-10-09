// Завдання 2: Парні та непарні
// Складність: O(n) час, O(1) пам'ять
// Гімназія №6, м. Дніпро

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n;
    cin >> n;
    
    int even = 0, odd = 0;
    for (int i = 0; i < n; i++) {
        int num;
        cin >> num;
        
        if (num % 2 == 0) {
            even++;
        } else {
            odd++;
        }
    }
    
    cout << even << " " << odd << endl;
    return 0;
}
