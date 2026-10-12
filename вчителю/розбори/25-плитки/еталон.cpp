// 25. Плитки — еталонний розв'язок (перебір дільників до √n парами).
// Час O(√n), пам'ять O(1).
#include <bits/stdc++.h>
using namespace std;

int main() {
    // n ≤ 10^12 не вміщується в int (до 2,1·10^9), тому long long (до 9,2·10^18)
    long long n;
    cin >> n;

    long long count = 0;  // кількість прямокутників = кількість дільників n (не більше 6720)
    long long best = 1;   // найбільший дільник, що не перевищує √n
    // i * i обчислюється в long long: i сягає 10^6, а i * i — 10^12.
    // Умова i * i <= n замість i <= sqrt(n): лише цілі числа, без похибок double.
    for (long long i = 1; i * i <= n; i++) {
        if (n % i == 0) {
            // пара дільників i і n / i: прямокутники i × (n / i) і (n / i) × i
            if (i == n / i)
                count += 1;  // точний квадрат: i × i — один прямокутник, а не два
            else
                count += 2;
            best = i;  // i зростає, тож наприкінці тут найближчий до √n дільник
        }
    }
    // Периметр сягає 2 · (1 + 10^12) ≈ 2·10^12 (для простого n) — теж long long
    long long perimeter = 2 * (best + n / best);
    cout << count << '\n' << perimeter << '\n';
    return 0;
}
