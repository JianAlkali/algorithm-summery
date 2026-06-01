**离散化**：将数据从较大的值域按原大小关系，映射到一个小且连续的值域。常用于数据预处理。
[[__封装物]]


# 直接复制版：
```cpp
// 离散化er：用于离散化数据
//
// 类型 T 需要：
// 默认构造 / 拷贝构造 / < / ==
//
// 使用流程：
// add ->
// build ->
// rank/get/inv_get
//
// 整体复杂度：
// build: O(n log n)
// 单次查询: O(log n)

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

DEFINE_CHECKER(CheckDiser,
    V(),              // 默认构造
    V(*(V*)0),        // 拷贝构造
    *(V*)0 < *(V*)0,  // <
    *(V*)0 == *(V*)0  // ==
)

template<class T, int N = (int)1e5 + 9>
struct Diser {
	// 若在这一行报错：类型 T 未实现所需运算符！
    typedef typename CheckDiser<T>::ASSERT _check;

    int n;
    T a[N];

    Diser() { reset(); }

    // 重置容器，用于多测试用例
    // O(1)
    void reset() {
        n = 0;
    }

    // 添加待离散化元素
    // 若超出容量返回 -1
    // O(1)
    int add(const T& x) {
        if (n >= N) return -1;
        a[n++] = x;
        return 0;
    }

    // 构建离散化表，必须在查询前调用
    // O(n log n)
    void build() {
        std::sort(a, a + n);
        n = std::unique(a, a + n) - a;
    }

    // 返回 x 的排名（1-based）
    // 若不存在，返回其应插入位置（仍为1-based）
    // O(log n)
    int rank(const T& x) const {
        return std::lower_bound(a, a + n, x) - a + 1;
    }

    // 返回 x 离散化后的索引（1-based）
    // 若不存在，返回 -pos（pos为插入位置1-based）
    // O(log n)
    int get(const T& x) const {
        auto it = std::lower_bound(a, a + n, x);
        int pos = (int)(it - a + 1);
        if (it == a + n || !(*it == x)) {
            return -pos;
        }
        return pos;
    }

    // 根据离散化索引（1-based）还原原始值
    // 若非法返回默认值 T{}
    // O(1)
    T inv_get(int idx) const {
        if (idx <= 0 || idx > n) return T{};
        return a[idx - 1];
    }

    // 返回去重后的元素个数
    // O(1)
    int size() const {
        return n;
    }
};

// 示例实例化
Diser<int, (int)1e5 + 9> diser;
```

---

# 现场抄写版：
```cpp
// 离散化er：用于离散化数据
//
// 使用流程：
// add ->
// build ->
// rank/get/inv_get
//
// 整体复杂度：
// build: O(n log n)
// 单次查询: O(log n)

struct Diser {
    int N = 1e5 + 9;
    int n;
    int a[N];

    Diser() { clear(); }

    // 重置容器，用于多测试用例
    // O(1)
    void clear() {
        n = 0;
    }

    // 添加待离散化元素
    // 若超出容量返回 -1
    // O(1)
    int add(int x) {
        if (n >= N) return -1;
        a[n++] = x;
        return 0;
    }

    // 构建离散化表，必须在查询前调用
    // O(n log n)
    void build() {
        sort(a, a + n);
        n = unique(a, a + n) - a;
    }

    // 返回 x 的排名（1-based）
    // 若不存在，返回其应插入位置（仍为1-based）
    // O(log n)
    int rank(int x) const {
        return lower_bound(a, a + n, x) - a + 1;
    }

    // 返回 x 离散化后的索引（1-based）
    // 若不存在，返回 -pos（pos为插入位置1-based）
    // O(log n)
    int get(int x) const {
        auto it = lower_bound(a, a + n, x);
        int pos = (int)(it - a + 1);
        if (it == a + n || !(*it == x)) {
            return -pos;
        }
        return pos;
    }

    // 根据离散化索引（1-based）还原原始值
    // 若非法返回默认值 -1
    // O(1)
    int inv_get(int idx) const {
        if (idx <= 0 || idx > n) return -1;
        return a[idx - 1];
    }

    // 返回去重后的元素个数
    // O(1)
    int size() const {
        return n;
    }
};

// 示例实例化
Diser diser;
```