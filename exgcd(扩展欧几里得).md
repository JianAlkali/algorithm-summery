[[数论]]

扩展欧几里得算法$O\left(log\left(min\left(a,b\right)\right)\right)$
注意，计算逆元时若模数不为质数，不能用费马，而只能用exgcd。
```cpp
// 返回 gcd(a, b)，并求出 ax + by = gcd(a, b) 的一组解 (x, y)
int exgcd(int a, int b, int &x, int &y) {
    if (b == 0) {
        x = 1; y = 0;
        return a;
    }    
    int d = exgcd(b, a % b, y, x);
    y -= a / b * x;
    return d;
}
// 求解线性同余方程 ax ≡ b (mod m)
// 返回最小非负整数解，如果无解返回 -1
// 在d!=1时有多解，其是等差的，每次增加t=m/d即下一个解。
int linear_congruence(int a, int b, int m) {
    int x, y;
    int d = exgcd(a, m, x, y);
    if (b % d != 0) return -1; // 无解
    // 调整解的范围
    int t = m / d;
    x = (1LL * x * (b / d) % t + t) % t;
    return x;
}
// 求a在模m下的逆元（要求gcd(a, m) = 1），无解返回 -1
// 这种方法求逆元比费马小定理qpow稍快，并且要求更宽松
int mod_inverse(int a, int m) {
    int x, y;
    int d = exgcd(a, m, x, y);    
    if (d != 1) return -1; // 逆元不存在
    return (x % m + m) % m; // 确保返回正数
}
```
