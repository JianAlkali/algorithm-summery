**算法**：树状数组结合差分思想，支持区间修改与单点查询，单次操作复杂度 `O(log n)`。
[[__封装物]]

# 直接复制版：

```cpp
// 树状数组：区间修改 + 单点查询
//
// 类型 T 需要：
// 默认构造 / 拷贝构造 / + / - / +=
//
// 使用流程：
// clear ->
// range_add ->
// get
//
// 整体复杂度：
// 单次操作 O(log n)

#ifndef DEFINE_CHECKER
#define DEFINE_CHECKER(name, ...) \
template<typename U> \
struct name { \
    template<typename V> \
    static char test(decltype((void)(__VA_ARGS__), 0)*); \
    template<typename V> \
    static int test(...); \
    enum { value = sizeof(test<U>(0)) == 1 }; \
    typedef char ASSERT[value ? 1 : -1]; \
};
#endif

DEFINE_CHECKER(CheckFenwick,
    V(),
    V(*(V*)0),
    *(V*)0 + *(V*)0,
    *(V*)0 - *(V*)0,
    *(V*)0 += *(V*)0
)

template<class T, int N = (int)1e5 + 9>
struct Fenwick {
    typedef typename CheckFenwick<T>::ASSERT _check;

    int n;
    T bit[N];

    Fenwick() { clear(); }

    // 重置
    // O(n)
    void clear(int _n = N - 1) {
        n = _n;
        for (int i = 0; i <= n; i++) bit[i] = T{};
    }

    // 单点增加
    // O(log n)
    int add(int pos, const T& val) {
        if (pos <= 0 || pos > n) return -1;
        for (int i = pos; i <= n; i += i & -i) {
            bit[i] += val;
        }
        return 0;
    }

    // 区间加 [l, r] += val
    // 若区间非法返回 -1
    // O(log n)
    int range_add(int l, int r, const T& val) {
        if (l > r || l < 1 || r > n) return -1;
        add(l, val);
        if (r + 1 <= n) add(r + 1, T{} - val);
        return 0;
    }

    // 查询前缀和
    // O(log n)
    T pre_sum(int pos) const {
        if (pos <= 0) return T{};
        if (pos > n) pos = n;
        T res = T{};
        for (int i = pos; i > 0; i -= i & -i) {
            res += bit[i];
        }
        return res;
    }

    // 查询单点值
    // O(log n)
    T get(int pos) const {
        if (pos <= 0 || pos > n) return T{};
        return pre_sum(pos);
    }
};

// 示例实例化
Fenwick<int, (int)1e5 + 9> bit;
```

---

# 现场抄写版：

```cpp
// 树状数组：区间修改 + 单点查询
//
// 使用流程：
// clear ->
// range_add ->
// get
//
// 整体复杂度：
// 单次操作 O(log n)

struct Fenwick {
    static const int N = 1e5 + 9;

    int n;
    int bit[N];

    Fenwick() { clear(); }

    void clear(int _n = N - 1) {
        n = _n;
        for (int i = 0; i <= n; i++) bit[i] = 0;
    }

    // 单点加
    int add(int pos, int val) {
        if (pos <= 0 || pos > n) return -1;
        for (int i = pos; i <= n; i += i & -i) {
            bit[i] += val;
        }
        return 0;
    }

    // 区间加
    // O(log n)
    int range_add(int l, int r, int val) {
        if (l > r || l < 1 || r > n) return -1;
        add(l, val);
        if (r + 1 <= n) add(r + 1, -val);
        return 0;
    }

    // 单点查询
    // O(log n)
    int get(int pos) {
        int res = 0;
        for (int i = pos; i > 0; i -= i & -i) {
            res += bit[i];
        }
        return res;
    }
};

// 示例实例化
Fenwick bit;
```