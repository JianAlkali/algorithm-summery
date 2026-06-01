**树状数组（Fenwick Tree）**：支持单点修改、前缀和查询，并可扩展到区间查询。代码短、常数小，是竞赛中最常用的数据结构之一。
[[__封装物]]

# 直接复制版：

```cpp
// 树状数组（Fenwick Tree）：维护前缀和
//
// 类型 T 需要：
// 默认构造 / 拷贝构造 / 支持 + 和 -
//
// 使用流程：
// clear ->
// add ->
// pre_sum / range_sum
//
// 整体复杂度：
// 单次 add / pre_sum / range_sum: O(log n)
// 空间复杂度：O(n)
//
// 默认：
// 1-base 索引
// range_sum(l, r) 查询闭区间 [l, r]

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
    V(),                // 默认构造
    V(*(V*)0),          // 拷贝构造
    *(V*)0 + *(V*)0,    // +
    *(V*)0 - *(V*)0     // -
)

template<class T, int N = (int)1e5 + 9>
struct Fenwick {
    // 若在这一行报错：类型 T 未实现所需运算符！
    typedef typename CheckFenwick<T>::ASSERT _check;

    int n;
    T tr[N];

    Fenwick() { clear(); }

    // 初始化为维护 [1, _n]
    // 若 _n 超出容量返回 -1
    // O(n)
    int init(int _n) {
        if (_n <= 0 || _n >= N) return -1;
        n = _n;
        for (int i = 1; i <= n; i++) tr[i] = T{};
        return 0;
    }

    // 清空结构，用于多测试用例
    // O(1)
    void clear() {
        n = 0;
    }

    // 单点增加：a[x] += v
    // 若下标非法返回 -1
    // O(log n)
    int add(int x, const T& v) {
        if (x <= 0 || x > n) return -1;
        for (int i = x; i <= n; i += i & -i) {
            tr[i] = tr[i] + v;
        }
        return 0;
    }

    // 查询前缀和 sum[1..x]
    // 若 x < 0 返回默认值 T{}
    // 若 x > n 自动截断到 n
    // O(log n)
    T pre_sum(int x) const {
        if (x < 0) return T{};
        if (x > n) x = n;
        T res = T{};
        for (int i = x; i > 0; i -= i & -i) {
            res = res + tr[i];
        }
        return res;
    }

    // 查询区间和 sum[l..r]
    // 若区间无交集返回默认值 T{}
    // O(log n)
    T range_sum(int l, int r) const {
        if (l > r) return T{};
        if (r < 1 || l > n) return T{};
        if (l < 1) l = 1;
        if (r > n) r = n;
        return pre_sum(r) - pre_sum(l - 1);
    }

    // 获取单点值 a[x]
    // 若下标非法返回默认值 T{}
    // O(log n)
    T get(int x) const {
        if (x <= 0 || x > n) return T{};
        return range_sum(x, x);
    }

    // 将 a[x] 增加到 val（即赋值）
    // 若下标非法返回 -1
    // O(log n)
    int set(int x, const T& val) {
        if (x <= 0 || x > n) return -1;
        return add(x, val - get(x));
    }
};

// 示例实例化
Fenwick<long long, (int)1e5 + 9> fw;
```

---

# 现场抄写版：
```cpp
// 树状数组（Fenwick Tree）：维护前缀和
//
// 使用流程：
// init ->
// add ->
// pre_sum / range_sum
//
// 整体复杂度：
// 单次 add / pre_sum / range_sum: O(log n)

struct Fenwick {
    static const int N = 1e5 + 9;

    int n;
    int tr[N];

    Fenwick() { clear(); }

    // 清空结构，用于多测试用例
    // O(1)
    void clear() {
        n = 0;
    }

    // 初始化为维护 [1, n]
    // O(n)
    void init(int _n) {
        n = _n;
        for (int i = 1; i <= n; i++) tr[i] = 0;
    }

    // 单点增加：a[x] += v
    // O(log n)
    void add(int x, int v) {
        for (int i = x; i <= n; i += i & -i) {
            tr[i] += v;
        }
    }

    // 查询前缀和 sum[1..x]
    // O(log n)
    int pre_sum(int x) const {
        int res = 0;
        for (int i = x; i > 0; i -= i & -i) {
            res += tr[i];
        }
        return res;
    }

    // 查询区间和 sum[l..r]
    // O(log n)
    int range_sum(int l, int r) const {
        if (l > r) return 0;
        return pre_sum(r) - pre_sum(l - 1);
    }

    // 获取单点值 a[x]
    // O(log n)
    int get(int x) const {
        return range_sum(x, x);
    }

    // 单点赋值：a[x] = v
    // O(log n)
    void set(int x, int v) {
        add(x, v - get(x));
    }
};

// 示例实例化
Fenwick fw;
```