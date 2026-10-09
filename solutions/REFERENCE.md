# 🔑 Teacher's Reference - Complete Solutions
**For:** Teachers and Instructors  
**Gymnasium:** №6, Dnipro  
**Language:** Ukrainian (Українська) + English  
**Year:** 2026

---

## 📌 Introduction

This reference contains **complete solutions** for all 7 problems in both **C++** and **Python**. Use this as:
- Grading guide for student submissions
- In-class demonstration material
- Source for alternative solution approaches

---

## ✅ Problem 1: Sum of Digits

### Problem:
Find the sum of all digits in a given number N.

**Example:** N=12345 → Output: 15 (1+2+3+4+5)

### C++ Solution:

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    long long n;
    cin >> n;
    
    int sum = 0;
    while (n > 0) {
        sum += n % 10;  // Add last digit
        n /= 10;        // Remove last digit
    }
    
    cout << sum << endl;
    return 0;
}
```

### Python Solution:

```python
#!/usr/bin/env python3

def sum_of_digits(n):
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total

# Alternative (more Pythonic):
# def sum_of_digits(n):
#     return sum(int(digit) for digit in str(n))

n = int(input())
print(sum_of_digits(n))
```

### Complexity:
- **Time:** O(log N) — number of digits
- **Space:** O(1)

### Test Cases:

| Input | Output | Explanation |
|-------|--------|-------------|
| 123 | 6 | 1+2+3 |
| 999 | 27 | 9+9+9 |
| 1 | 1 | Single digit |
| 1000 | 1 | 1+0+0+0 |
| 505 | 10 | 5+0+5 |

### Common Student Mistakes:
- ❌ Using `int` instead of `long long` (overflow)
- ❌ Infinite loop: forgetting `n /= 10`
- ❌ Wrong modulo: using `% 100` instead of `% 10`

---

## ✅ Problem 2: Even and Odd

### Problem:
Count even and odd numbers in a list.

**Example:** [1,2,3,4,5] → Output: 2 even, 3 odd

### C++ Solution:

```cpp
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
```

### Python Solution:

```python
#!/usr/bin/env python3

n = int(input())
numbers = list(map(int, input().split()))

even = sum(1 for num in numbers if num % 2 == 0)
odd = n - even

print(f"{even} {odd}")
```

### Test Cases:

| Input | Output |
|-------|--------|
| 5; [1,2,3,4,5] | 2 3 |
| 4; [10,20,30,40] | 4 0 |
| 3; [-1,-2,-3] | 1 2 |

---

## ✅ Problem 3: Pyramid

### Problem:
Print a pyramid with N rows, where row i contains numbers 1 to i.

**Example:** N=3 → Output: 1 / 1 2 / 1 2 3

### C++ Solution:

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n;
    cin >> n;
    
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            cout << j;
            if (j < i) cout << " ";
        }
        cout << "\n";
    }
    
    return 0;
}
```

### Python Solution:

```python
#!/usr/bin/env python3

n = int(input())

for i in range(1, n + 1):
    print(" ".join(str(j) for j in range(1, i + 1)))
```

### Complexity:
- **Time:** O(N²) — nested loops
- **Space:** O(1)

### Test Cases:

| N | Output |
|---|--------|
| 1 | 1 |
| 2 | 1 / 1 2 |
| 3 | 1 / 1 2 / 1 2 3 |
| 4 | 1 / 1 2 / 1 2 3 / 1 2 3 4 |

---

## ✅ Problem 4: Palindrome Check

### Problem:
Check if a string is a palindrome (ignore case).

**Example:** "racecar" → YES, "hello" → NO

### C++ Solution:

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    string s;
    cin >> s;
    
    // Convert to lowercase
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
    
    cout << (is_palindrome ? "YES" : "NO") << endl;
    return 0;
}
```

### Python Solution:

```python
#!/usr/bin/env python3

s = input().lower()

if s == s[::-1]:
    print("YES")
else:
    print("NO")
```

### Complexity:
- **Time:** O(N) — single pass
- **Space:** O(N) — string storage

### Test Cases:

| Input | Output |
|-------|--------|
| racecar | YES |
| hello | NO |
| Aba | YES |
| 121 | YES |
| a | YES |

---

## ✅ Problem 5: Find Minimum

### Problem:
Find the minimum value in an array.

**Example:** [5,2,8,1,9] → 1

### C++ Solution:

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n;
    cin >> n;
    
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    
    int min_val = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] < min_val) {
            min_val = arr[i];
        }
    }
    
    cout << min_val << endl;
    return 0;
}

// Or using STL:
// int min_val = *min_element(arr.begin(), arr.end());
```

### Python Solution:

```python
#!/usr/bin/env python3

n = int(input())
numbers = list(map(int, input().split()))

print(min(numbers))
```

### Test Cases:

| Input | Output |
|-------|--------|
| 5; [3,7,2,9,1] | 1 |
| 3; [-5,-10,-2] | -10 |
| 1; [42] | 42 |

---

## ✅ Problem 6: Anagrams

### Problem:
Check if two strings are anagrams (ignore case).

**Example:** "listen", "silent" → YES

### C++ Solution:

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    string s1, s2;
    cin >> s1 >> s2;
    
    // Convert to lowercase
    for (char& c : s1) c = tolower(c);
    for (char& c : s2) c = tolower(c);
    
    // Different lengths = not anagrams
    if (s1.length() != s2.length()) {
        cout << "NO" << endl;
        return 0;
    }
    
    // Sort and compare
    sort(s1.begin(), s1.end());
    sort(s2.begin(), s2.end());
    
    cout << (s1 == s2 ? "YES" : "NO") << endl;
    return 0;
}
```

### Python Solution:

```python
#!/usr/bin/env python3

s1 = input().lower()
s2 = input().lower()

if sorted(s1) == sorted(s2):
    print("YES")
else:
    print("NO")
```

### Complexity:
- **Time:** O(N log N) — sorting dominates
- **Space:** O(N) — sorted strings

### Test Cases:

| Input 1 | Input 2 | Output |
|---------|---------|--------|
| listen | silent | YES |
| hello | world | NO |
| abc | cab | YES |
| ABA | Baa | YES |

---

## ✅ Problem 7: Fibonacci Sequence

### Problem:
Print first N Fibonacci numbers.

**Example:** N=7 → 0 1 1 2 3 5 8

### C++ Solution:

```cpp
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
```

### Python Solution:

```python
#!/usr/bin/env python3

n = int(input())

a, b = 0, 1
result = []

for _ in range(n):
    result.append(a)
    a, b = b, a + b

print(" ".join(map(str, result)))
```

### Complexity:
- **Time:** O(N)
- **Space:** O(N) for output

### Test Cases:

| N | Output |
|---|--------|
| 1 | 0 |
| 2 | 0 1 |
| 5 | 0 1 1 2 3 |
| 7 | 0 1 1 2 3 5 8 |
| 10 | 0 1 1 2 3 5 8 13 21 34 |

---

## 📊 Complexity Comparison

| Problem | C++ Complexity | Python | Difficulty |
|---------|----------------|--------|-----------|
| 1 | O(log N) | O(log N) | ⭐ Easy |
| 2 | O(N) | O(N) | ⭐ Easy |
| 5 | O(N) | O(N) | ⭐ Easy |
| 3 | O(N²) | O(N²) | ⭐⭐ Medium |
| 4 | O(N) | O(N) | ⭐⭐ Medium |
| 6 | O(N log N) | O(N log N) | ⭐⭐ Medium |
| 7 | O(N) | O(N) | ⭐⭐⭐ Hard |

---

## 🎓 Pedagogical Notes

### For Teaching:

1. **Problem 1-2-5:** Teach basics (loops, conditionals, arrays)
2. **Problem 3-4-6:** Introduce strings and nested structures
3. **Problem 7:** Show optimization and sequences

### Common Student Issues:

| Issue | Solution |
|-------|----------|
| Overflow errors | Use `long long` instead of `int` |
| Off-by-one errors | Print loop trace on paper |
| Wrong output format | Check spacing and newlines |
| Infinite loops | Add debug output to see value changes |
| Logic errors | Write pseudocode first |

### Grading Rubric:

- **100%:** All test cases pass, clean code
- **70%:** Most test cases pass, minor issues
- **50%:** Half correct, significant logic error
- **25%:** Partial attempt, correct approach
- **0%:** No submission or syntax error

---

## 📚 References

- **Codeforces:** https://codeforces.com/
- **CP-Algorithms:** https://cp-algorithms.com/
- **Python Docs:** https://docs.python.org/3/
- **C++ Reference:** https://en.cppreference.com/

---

**Last Updated:** October 2026  
**Version:** 1.0  
**Reviewed:** ✅

*For use by teachers at Gymnasium №6, Dnipro and other educational institutions*
