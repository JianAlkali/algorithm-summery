**算法**：线段树（Lazy Segment Tree）支持模意义下的区间加、区间乘、区间赋值和区间求和。内部统一将操作表示为仿射变换 `x -> x * mul + add (mod MOD)`，赋值操作等价于 `mul = 0, add = val`。单次操作复杂度 `O(log n)`。
[[__封装物]]

# 直接复制版：

```cpp
// 线段树：模意义下区间加 / 区间乘 / 区间赋值 / 区间求和
//
// 使用流程：
// clear ->
// build ->
// {
// range_add / range_mul / range_set ->
// query ->
// }
//
// 整体复杂度：
// build: O(n)
// 单次操作: O(log n)
//
// 懒标记说明：
// 每个区间维护变换 x -> x * lazy_mul + lazy_add (mod MOD)
// 初始 lazy_mul = 1, lazy_add = 0
// 区间赋值为 val 等价于：lazy_mul = 0, lazy_add = val

template<int N = (int)1e5 + 9, int MOD = 998244353>
struct SegTree {
    int n;
    int sum[N << 2];
    int lazy_mul[N << 2];
    int lazy_add[N << 2];

    SegTree() { clear(); }

    // 取模到 [0, MOD)
    // O(1)
    int norm(int x) const {
        x %= MOD;
        if (x < 0) x += MOD;
        return x;
    }

    // 重置整棵树
    // O(N)
    void clear(int _n = 0) {
        n = _n;
        for (int i = 0; i < (N << 2); i++) {
            sum[i] = 0;
            lazy_mul[i] = 1;
            lazy_add[i] = 0;
        }
    }

    // 将区间 [l, r] 应用变换 x -> x * mul + add
    // O(1)
    void _apply(int p, int l, int r, int mul, int add) {
        int len = r - l + 1;
        sum[p] = (sum[p] * mul + 1LL * add * len) % MOD;
        lazy_mul[p] = 1LL * lazy_mul[p] * mul % MOD;
        lazy_add[p] = (1LL * lazy_add[p] * mul + add) % MOD;
    }

    // 下传懒标记
    // O(1)
    void _push(int p, int l, int r) {
        if (l == r) return;
        if (lazy_mul[p] == 1 && lazy_add[p] == 0) return;

        int mid = (l + r) >> 1;
        _apply(p << 1, l, mid, lazy_mul[p], lazy_add[p]);
        _apply(p << 1 | 1, mid + 1, r, lazy_mul[p], lazy_add[p]);

        lazy_mul[p] = 1;
        lazy_add[p] = 0;
    }

    // 向上更新
    // O(1)
    void _pull(int p) {
        sum[p] = sum[p << 1] + sum[p << 1 | 1];
        if (sum[p] >= MOD) sum[p] -= MOD;
    }

    // 用 a[1..n] 建树（1-base）
    // O(n)
    void build(int p, int l, int r, const int a[]) {
        lazy_mul[p] = 1;
        lazy_add[p] = 0;
        if (l == r) {
            sum[p] = norm(a[l]);
            return;
        }
        int mid = (l + r) >> 1;
        build(p << 1, l, mid, a);
        build(p << 1 | 1, mid + 1, r, a);
        _pull(p);
    }

    // 建树
    // 若 n 非法返回 -1
    // O(n)
    int build(int _n, const int a[]) {
        if (_n <= 0 || _n >= N) return -1;
        n = _n;
        build(1, 1, n, a);
        return 0;
    }

    // 区间应用仿射变换
    // O(log n)
    void _update(int p, int l, int r, int ql, int qr, int mul, int add) {
        if (ql <= l && r <= qr) {
            _apply(p, l, r, mul, add);
            return;
        }
        _push(p, l, r);
        int mid = (l + r) >> 1;
        if (ql <= mid) _update(p << 1, l, mid, ql, qr, mul, add);
        if (qr > mid) _update(p << 1 | 1, mid + 1, r, ql, qr, mul, add);
        _pull(p);
    }

    // 区间加
    // 若区间非法返回 -1
    // O(log n)
    int range_add(int l, int r, int val) {
        if (l > r || l < 1 || r > n) return -1;
        _update(1, 1, n, l, r, 1, norm(val));
        return 0;
    }

    // 区间乘
    // 若区间非法返回 -1
    // O(log n)
    int range_mul(int l, int r, int val) {
        if (l > r || l < 1 || r > n) return -1;
        _update(1, 1, n, l, r, norm(val), 0);
        return 0;
    }

    // 区间赋值
    // 若区间非法返回 -1
    // O(log n)
    int range_set(int l, int r, int val) {
        if (l > r || l < 1 || r > n) return -1;
        _update(1, 1, n, l, r, 0, norm(val));
        return 0;
    }

    // 查询区间和
    // 若区间非法返回 -1
    // O(log n)
    int _query(int p, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return sum[p];
        _push(p, l, r);
        int mid = (l + r) >> 1;
        int res = 0;
        if (ql <= mid) res = (res + _query(p << 1, l, mid, ql, qr)) % MOD;
        if (qr > mid) res = (res + _query(p << 1 | 1, mid + 1, r, ql, qr)) % MOD;
        return res;
    }

    // 查询区间和
    // 若区间非法返回 -1
    // O(log n)
    int query(int l, int r) {
        if (l > r || l < 1 || r > n) return -1;
        return _query(1, 1, n, l, r);
    }
};

// 示例实例化
SegTree<(int)1e5 + 9, 998244353> seg;
```

---

# 现场抄写版：

```cpp
// 线段树：区间加 / 区间乘 / 区间赋值 / 区间求和（mod MOD）
struct SegTree {
    static const int N = 1e5 + 9;
    static const int MOD = 998244353;

    int n;
    int sum[N << 2], mul[N << 2], add[N << 2];

    void clear(int _n) {
        n = _n;
        for (int i = 0; i < (N << 2); i++) {
            sum[i] = 0;
            mul[i] = 1;
            add[i] = 0;
        }
    }

    int norm(int x) {
        x %= MOD;
        if (x < 0) x += MOD;
        return x;
    }

    void apply(int p, int l, int r, int m, int a) {
        sum[p] = (sum[p] * m + 1LL * a * (r - l + 1)) % MOD;
        mul[p] = 1LL * mul[p] * m % MOD;
        add[p] = (1LL * add[p] * m + a) % MOD;
    }

    void push(int p, int l, int r) {
        if (mul[p] == 1 && add[p] == 0) return;
        int mid = (l + r) >> 1;
        apply(p << 1, l, mid, mul[p], add[p]);
        apply(p << 1 | 1, mid + 1, r, mul[p], add[p]);
        mul[p] = 1;
        add[p] = 0;
    }

    void pull(int p) {
        sum[p] = (sum[p << 1] + sum[p << 1 | 1]) % MOD;
    }

    void build(int p, int l, int r, int a[]) {
        mul[p] = 1;
        add[p] = 0;
        if (l == r) {
            sum[p] = norm(a[l]);
            return;
        }
        int mid = (l + r) >> 1;
        build(p << 1, l, mid, a);
        build(p << 1 | 1, mid + 1, r, a);
        pull(p);
    }

    void update(int p, int l, int r, int ql, int qr, int m, int a) {
        if (ql <= l && r <= qr) {
            apply(p, l, r, m, a);
            return;
        }
        push(p, l, r);
        int mid = (l + r) >> 1;
        if (ql <= mid) update(p << 1, l, mid, ql, qr, m, a);
        if (qr > mid) update(p << 1 | 1, mid + 1, r, ql, qr, m, a);
        pull(p);
    }

    int query(int p, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return sum[p];
        push(p, l, r);
        int mid = (l + r) >> 1;
        int res = 0;
        if (ql <= mid) res = (res + query(p << 1, l, mid, ql, qr)) % MOD;
        if (qr > mid) res = (res + query(p << 1 | 1, mid + 1, r, ql, qr)) % MOD;
        return res;
    }

    // [l, r] += v
    void range_add(int l, int r, int v) {
        update(1, 1, n, l, r, 1, norm(v));
    }

    // [l, r] *= v
    void range_mul(int l, int r, int v) {
        update(1, 1, n, l, r, norm(v), 0);
    }

    // [l, r] = v
    void range_set(int l, int r, int v) {
        update(1, 1, n, l, r, 0, norm(v));
    }

    // 查询区间和
    int query(int l, int r) {
        return query(1, 1, n, l, r);
    }
};

// 示例实例化
SegTree seg;
```