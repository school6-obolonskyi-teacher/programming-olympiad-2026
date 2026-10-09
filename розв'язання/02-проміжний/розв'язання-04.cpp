// Завдання 4: Паліндром
// Складність: O(n) час, O(1) пам'ять
// Гімназія №6, м. Дніпро

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    string s;
    cin >> s;
    
    for (char& c : s) {
        c = tolower(c);
    }
    
    bool is_palindrome = true;
    int n = s.length();
    
    for (int i = 0; i < n / 2; i++) {
        if (s[i] != s[n - 1 - i]) {
            is_palindrome = false;
            break;
        }
    }
    
    cout << (is_palindrome ? "ТАК" : "НІ") << endl;
    return 0;
}
