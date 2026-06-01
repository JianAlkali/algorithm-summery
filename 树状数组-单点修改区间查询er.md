**算法**：树状数组（Fenwick Tree）用于维护前缀和，支持单点修改与区间查询，单次操作复杂度 `O(log n)`。
[[__封装物]]

# 直接复制版：

```cpp
// 树状数组：单点修改 + 区间查询
//
// 类型 T 需要：
// 默认构造 / 拷贝构造 / + / - / +=
//
// 使用流程：
// clear ->
// add ->
// pre_sum / range_sum
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

    // 单点增加 val
    // 若位置非法返回 -1
    // O(log n)
    int add(int pos, const T& val) {
        if (pos <= 0 || pos > n) return -1;
        for (int i = pos; i <= n; i += i & -i) {
            bit[i] += val;
        }
        return 0;
    }

    // 查询前缀和 [1, pos]
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

    // 查询区间和 [l, r]
    // O(log n)
    T range_sum(int l, int r) const {
        if (l > r) return T{};
        return pre_sum(r) - pre_sum(l - 1);
    }
};

// 示例实例化
Fenwick<int, (int)1e5 + 9> bit;
```

---

# 现场抄写版：

```cpp
// 树状数组：单点修改 + 区间查询
//
// 使用流程：
// clear ->
// add ->
// pre_sum / range_sum
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
    // O(log n)
    int add(int pos, int val) {
        if (pos <= 0 || pos > n) return -1;
        for (int i = pos; i <= n; i += i & -i) {
            bit[i] += val;
        }
        return 0;
    }

    // 前缀和 [1, pos]
    // O(log n)
    int pre_sum(int pos) {
        int res = 0;
        for (int i = min(pos, n); i > 0; i -= i & -i) {
            res += bit[i];
        }
        return res;
    }

    // 区间和 [l, r]
    // O(log n)
    int range_sum(int l, int r) {
        return pre_sum(r) - pre_sum(l - 1);
    }
};

// 示例实例化
Fenwick bit;
```