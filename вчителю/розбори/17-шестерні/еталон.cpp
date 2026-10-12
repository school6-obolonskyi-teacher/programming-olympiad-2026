// 17. Шестерні — еталонний розв'язок (алгоритм Евкліда).
// Час O(log min(a, b)), пам'ять O(1).
#include <bits/stdc++.h>
using namespace std;

// НСД(a, b) = НСД(b, a mod b), НСД(a, 0) = a
long long gcd_euclid(long long a, long long b) {
    while (b != 0) {
        long long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

int main() {
    // a, b ≤ 10^9 вміщуються в int, але НСК сягає a · b ≤ 10^18,
    // тому всі обчислення ведемо в long long (до 9,2·10^18)
    long long a, b;
    cin >> a >> b;
    long long g = gcd_euclid(a, b);
    // Ділимо ДО множення: a / g * b. Проміжне значення a / g не перевищує a,
    // а результат — це сама відповідь, тож переповнення не буде.
    long long l = a / g * b;
    cout << g << ' ' << l << '\n';
    return 0;
}
