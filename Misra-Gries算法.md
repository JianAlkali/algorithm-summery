[[动态规划]]

该算法用于查询频次大于某个比例的元素。普通版本：可动态添加元素、查询整个区间；线段树版本：不支持动态修改，支持任意区间查询。与莫队相比，它的普通版本可以动态添加元素，边查边改。可能误报，但不会漏报，需要搭配二分验证。
普通版本我没写过，这里给个AI的：process $O\left(K\right)$，query $O\left(K+ n\right)$
```cpp
class TrafficMonitor {
    unordered_map<string, int> counters;  // IP -> 计数
    int total_packets = 0;
    const int k = 100;  // 找频率 > 1% 的元素
    void process(const string& ip) {
        total_packets++;
        // Misra-Gries 更新逻辑
        if (counters.count(ip)) {
            counters[ip]++;
        } else if (counters.size() < k - 1) {
            counters[ip] = 1;
        } else {
            // 消去操作
            vector<string> to_remove;
            for (auto& [ip_val, cnt] : counters) {
                if (--cnt == 0) to_remove.push_back(ip_val);
            }
            for (const auto& ip_val : to_remove) {
                counters.erase(ip_val);
            }
        }
    }
    vector<string> query() {
        vector<string> result;
        double threshold = total_packets * 0.01;
        for (const auto& [ip, cnt] : counters) {
            if (cnt > threshold)
                result.push_back(ip);
        }
        sort(result.begin(), result.end());
        return result;
    }
};
```

线段树版本： 构造 $O\left(n⋅ n⋅K^{2}\right)$, 查询 $O\left( n⋅K^{2}\right)$
```cpp
constexpr int K=2; // 要寻找的频次K再-1，比如寻找频次>len/3的元素，K取2
#define ls(x) ((x)<<1)
#define rs(x) (((x)<<1)|1)
#define mid(l,r) (((l)+(r))>>1)
struct Seg{
    using kpii=pii[K];
    pii t[N<<2][K];
    int n;
    inl void modify(kpii &x, int p){ // 保证频次递减排序
        for(int i=p-1;i>=0;i--){
            if(x[i].first<x[i+1].first)
                swap(x[i],x[i+1]);
            else return;
        }
    }
    inl void in_merge(kpii &x, pii w){ // 单w并入x O(K)
        if(w.first==0) return;
        for(int i=0;i<K;i++){ //同类合并
            if(x[i].second==w.second){
                x[i].first+=w.first;
                modify(x,i);
                return;
            }
        }
        for(int i=0;i<K;i++){ //空位插入
            if(x[i].first==0){
                x[i]=w;
                modify(x,i);
                return;
            }
        }
        // 满位消除
        int mi=w.first;
        for(int i=K-1;i>=0;i--){
            if(x[i].first){
                mi=min(mi,x[i].first);
                break;
            }
        }
```

```cpp
        for(int i=0;i<K;i++){
            x[i].first-=mi;
        }
        w.first-=mi;
        if(!w.first)
            return;
        for(int i=0;i<K;i++){
            if(x[i].first==0){
                x[i]=w;
                modify(x,i);
                return;
            }
        }
    }
    inl void merge(const kpii& a,const kpii& b, kpii& r){ // 两个节点合并 O(K^2)
        if(a!=r)
            copy(a,a+K,r);
        for(int i=0;i<K && b[i].first;i++)
            in_merge(r,b[i]);
    }
    inl void pushup(int x){
        merge(t[ls(x)],t[rs(x)],t[x]);
    }
    inl void set(int x,int l,int r,int a[N]){ // *该线段树不支持更新 O(nlognK^2)
        if(l==r){
            t[x][0]={1,a[l]}; return;
        }
        int m=mid(l,r);
        set(ls(x),l,m,a);
        set(rs(x),m+1,r,a);
        pushup(x);
}
inl void query(int x,int l,int r,int ql,int qr, kpii& res){ //O(lognK^2)
    if(ql<=l && r<=qr){
        merge(res,t[x],res); return;
    }
    int m=mid(l,r);
    if(m>=ql) query(ls(x),l,m,ql,qr,res);
    if(m<qr) query(rs(x),m+1,r,ql,qr,res);
}
```

```cpp
    // 外部接口：
    inl void rebuild(int a[N], int _n){ //多测更新
        n=_n;
        for(int i=0, ed=(n+1)<<2;i<ed;i++)
            fill(t[i],t[i]+K,pii{0,0});
        set(1,1,n,a);
    }
    inl vi query(int l,int r){
        kpii res;
        query(1,1,n,l,r,res);
        vi ans(K);
        for(int i=0;i<K;i++){
            if(res[i].first)
                ans.emplace_back(res[i].second);
            else
                break;
        }
        return ans;
    }
}seg;
```

调用示例：（输入、输出部分略）
```cpp
map<int,vector<int>> pos; //存储元素位置，用于二分精确计数
    for(int i=1;i<=n;i++)
        pos[a[i]].emplace_back(i);
    seg.rebuild(a,n);
    auto che=[&](int x,int l,int r)->int{ //二分检验，返回频次
        const auto& ve=pos[x];
        return upper_bound(ve.begin(),ve.end(),r)-lower_bound(ve.begin(),ve.end(),l);
    };
    for(int i=0,l,r;i<q;i++){ //处理查询
        cin>>l>>r;
        int tsh=(r-l+1)/3;
        auto ans=seg.query(l,r);
        for(int i=ans.size()-1;i>=0;i--)
            if(che(ans[i],l,r)<=tsh) //检验发现不合法
                swap(ans[i],ans.back()), ans.pop_back(); //删除 
```
