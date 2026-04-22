[[_封装物]]
```cpp
// 增量最短路（静态邻接表 + 动态激活版本）
//
// W 需要支持：
// 默认构造 / 拷贝构造 / < / == / +
//
// 使用流程：
// reset -> add_edge / add_source -> activate -> run
//
// 复杂度：
// reset: O(n)
// add_edge: O(1)
// activate: O(in_deg + log V)
// run: O((V + E) log V)

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

DEFINE_CHECKER(CheckISP,
    V(),
    V(*(V*)0),
    *(V*)0 < *(V*)0,
    *(V*)0 == *(V*)0,
    *(V*)0 + *(V*)0
)

template<class W, W INF, int N = 100000 + 9, int M = 200000 + 9>
struct IncrementalShortestPath {
	// 若在这一行报错：类型 W 未实现所需运算符！
    typedef typename CheckISP<W>::ASSERT _check;

    struct Edge {
        int to, next;
        W w;

        Edge() : to(0), next(-1), w(W{}) {}
        Edge(int to_, int next_, const W& w_) : to(to_), next(next_), w(w_) {}
    };

    int n, ecnt;

    Edge out[M];
    int head_out[N];

    Edge in[M];
    int head_in[N];

    W dist[N];
    bool active[N];

    struct Node {
        W d;
        int id;

        Node() : d(W{}), id(0) {}
        Node(const W& d_, int id_) : d(d_), id(id_) {}

        bool operator>(const Node& other) const {
            return other.d < d;
        }
    };

    std::priority_queue<Node, std::vector<Node>, std::greater<Node>> pq;

    IncrementalShortestPath() { reset(0); }

    // 重置并初始化图
    // 返回：void
    // 复杂度：O(n)
    void reset(int n_) {
        n = n_;
        ecnt = 0;

        for (int i = 0; i <= n; i++) {
            head_out[i] = -1;
            head_in[i] = -1;
            dist[i] = INF;
            active[i] = false;
        }

        while (!pq.empty()) pq.pop();
    }

    // 添加有向边 u -> v
    // 返回：void
    // 复杂度：O(1)
    void add_edge(int u, int v, const W& w) {
        out[ecnt] = Edge(v, head_out[u], w);
        head_out[u] = ecnt;

        in[ecnt] = Edge(u, head_in[v], w);
        head_in[v] = ecnt;

        ecnt++;
    }

    // 添加源点
    // 返回：void
    // 复杂度：O(log V)
    void add_source(int s, const W& d = W{}) {
        if (d < dist[s]) {
            dist[s] = d;
            active[s] = true;
            pq.push(Node(d, s));
        }
    }

    // 激活节点 x，并尝试用入边更新
    // 返回：void
    // 复杂度：O(in_deg(x) + log V)
    void activate(int x) {
        if (active[x]) return;
        active[x] = true;

        W best = dist[x];

        for (int i = head_in[x]; i != -1; i = in[i].next) {
            int y = in[i].to;
            if (!active[y]) continue;

            W nd = dist[y] + in[i].w;
            if (nd < best) best = nd;
        }

        if (best < dist[x]) {
            dist[x] = best;
            pq.push(Node(best, x));
        }
    }

    // 执行增量最短路
    // 返回：void
    // 复杂度：O((V + E) log V)
    void run() {
        while (!pq.empty()) {
            Node cur = pq.top(); pq.pop();

            int u = cur.id;
            W d = cur.d;

            if (!(d == dist[u])) continue;
            if (d == INF) continue;

            for (int i = head_out[u]; i != -1; i = out[i].next) {
                int v = out[i].to;
                if (!active[v]) continue;

                W nd = d + out[i].w;

                if (nd < dist[v]) {
                    dist[v] = nd;
                    pq.push(Node(nd, v));
                }
            }
        }
    }

    // 获取最短路
    // 返回：dist[x]
    // 复杂度：O(1)
    W get_dist(int x) const {
        return dist[x];
    }

    // 判断是否可达
    // 返回：true=可达 / false=不可达
    // 复杂度：O(1)
    bool reachable(int x) const {
        return !(dist[x] == INF);
    }

    // 当前点数
    // 返回：n
    // 复杂度：O(1)
    int size() const {
        return n;
    }
};

// 示例
IncrementalShortestPath<long long, (long long)4e18, 100000 + 9, 200000 + 9> isp;
```