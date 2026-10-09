// Завдання 6: Анаграми
// Складність: O(n log n) час, O(n) пам'ять
// Гімназія №6, м. Дніпро

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    string s1, s2;
    cin >> s1 >> s2;
    
    for (char& c : s1) c = tolower(c);
    for (char& c : s2) c = tolower(c);
    
    if (s1.length() != s2.length()) {
        cout << "НІ" << endl;
        return 0;
    }
    
    sort(s1.begin(), s1.end());
    sort(s2.begin(), s2.end());
    
    cout << (s1 == s2 ? "ТАК" : "НІ") << endl;
    return 0;
}
