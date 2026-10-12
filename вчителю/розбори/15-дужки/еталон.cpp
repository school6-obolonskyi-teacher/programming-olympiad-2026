// 15. Дужки — еталонний розв'язок (стек).
// Час O(n), пам'ять O(n).
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    // Стек відкритих дужок, які ще чекають на свою пару.
    // string має push_back / back / pop_back, тож працює як стек символів.
    string st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            st.push_back(c);
        } else {
            char need = (c == ')') ? '(' : (c == ']') ? '[' : '{';
            // Закривна дужка має закрити саме ОСТАННЮ відкриту, і того самого типу.
            // Перевірка st.empty() обов'язкова: back() порожнього рядка — невизначена поведінка.
            if (st.empty() || st.back() != need) {
                cout << "NO\n";
                return 0;
            }
            st.pop_back();
        }
    }
    // Наприкінці не повинно лишитися незакритих дужок
    cout << (st.empty() ? "YES" : "NO") << '\n';
    return 0;
}
