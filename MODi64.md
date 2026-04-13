[[_其他技巧&我的小东西]]

实现内部模意义下运算
```cpp
struct MODi64 {
    using i64 = long long;
    using i128 = __int128_t;
    static i64 MOD; // 运行时模数
i64 v;
    static i64 norm(i64 x) {
        if (x >= MOD || x < 0) {
            x %= MOD;
            if (x < 0) x += MOD;
        }
        return x;
    }
    MODi64(): v(0) {}
    MODi64(i64 x): v(norm(x)) {}
    static void set_mod(i64 m) {
        MOD = m;
}
    // 一元运算符重载
    MODi64& operator+=(const MODi64& o) {
        v += o.v;
        if (v >= MOD) v -= MOD;
        return *this;
    }
    MODi64& operator-=(const MODi64& o) {
        v -= o.v;
        if (v < 0) v += MOD;
        return *this;
    }
    MODi64& operator*=(const MODi64& o) {
        v = (i128)v * o.v % MOD;
        return *this;
    }
    MODi64 operator-() const {
        return MODi64(v ? MOD - v : 0);
    }

    // 扩展欧几里得求逆
    static i64 exgcd(i64 a, i64 b, i64& x, i64& y) {
        if (!b) {
            x = 1; y = 0;
            return a;
        }
        i64 g = exgcd(b, a % b, y, x);
        y -= (a / b) * x;
        return g;
    }
    MODi64 inv() const {
        i64 x, y;
        i64 g = exgcd(v, MOD, x, y); // 通常稍快于qpow求逆
        assert(g == 1); // 不互质时无逆元
        return MODi64(x);
    }
    MODi64& operator/=(const MODi64& o) {
        return (*this) *= o.inv();
    }
    // 二元运算符
    friend MODi64 operator+(MODi64 a, const MODi64& b) { return a += b; }
    friend MODi64 operator-(MODi64 a, const MODi64& b) { return a -= b; }
    friend MODi64 operator*(MODi64 a, const MODi64& b) { return a *= b; }
    friend MODi64 operator/(MODi64 a, const MODi64& b) { return a /= b; }
    // 比较运算符
    friend bool operator==(const MODi64& a, const MODi64& b) { return a.v == b.v; }
    friend bool operator!=(const MODi64& a, const MODi64& b) { return a.v != b.v; }

    // 快速幂
    static MODi64 pow(MODi64 a, long long e) {
        MODi64 r = 1;
        while (e > 0) {
            if (e & 1) r *= a;
            a *= a;
            e >>= 1;
        }
        return r;
    }
    // IO 支持
    friend ostream& operator<<(ostream& os, const MODi64& x) {
        return os << x.v;
    }
    friend istream& operator>>(istream& is, MODi64& x) {
        i64 t;
        is >> t;
        x = MODi64(t);
        return is;
    }
};
MODi64::i64 MODi64::MOD = 998244353; // MOD默认值
```
