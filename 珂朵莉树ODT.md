[[_数据结构]]
**珂朵莉树（又称老司机树 Old Driver Tree ODT，或颜色段均摊）** 是一种用于高效混杂区间操作 且 区间数量趋于较小的值下，的一种区间信息的数据结构。
在数据完全随机，且有**区间赋值**这类能够降低区间段数的操作情况下，珂朵莉树可以按值维护区间，区间数量不会很大。
支持的区间操作：`set` `+` `*` `MOD` `getsum(a)` `getsum(a^x%y)` `get第k小`...
用`set` `map`实现时，其复杂度为 $O(n \cdot \log(\log(n)))$（实际中由于`set` `map`常数较大，常当成 $O(n\cdot \log(n))$ 计算，如果有单次 $O(\log(n))$ 的操作，复杂度再乘上`log`即可。

以下是一个解决[cf珂朵莉树原题 - 896C](https://codeforces.com/problemset/problem/896/C)的珂朵莉树解法：
```cpp
struct Data{
    int l;
    mutable int r,v; // mutable用于对const迭代器的值修改 也可用map实现
    const bool operator<(const Data& o) const {
        return l<o.l;
    }
};
set<Data> odt;

int seed;
int rnd(){ // 题目的随机生成器
    int ret = seed;
    seed = (seed*7+13)%MOD;
    return ret;
}

// 用于将区间分割出一个以p点开始的区间
auto split(int p){
    if(p>odt.rbegin()->r)
        return odt.end(); // p==n+1 or gt
    auto it=odt.upper_bound(Data{p,0,0});
    --it;
    if(it->l==p)
        return it;
    int l=it->l, m=p, r=it->r, val=it->v;
    odt.erase(it);
    odt.emplace(Data{l,m-1,val});
    return odt.emplace(Data{m,r,val}).first;
}

// 获取[l,r]区间的区间 使用for遍历[it,ed)即可遍历[l,r]
auto split_get(int l,int r){
    auto ed=split(r+1);
    auto it=split(l);
    return make_pair(it,ed);
}

pii tmp[N]; // 用于区间第k小 临时数组
void solve(){
    int n,m,vm;
    cin>>n>>m>>seed>>vm;
    {
        auto it=odt.end();
        for(int i=1;i<=n;i++){
            int a=(rnd()%vm)+1;
            it=odt.emplace_hint(it,Data{i,i,a});
        }
    }
    
    for(int i=1;i<=m;i++){
        int op=(rnd()%4)+1, l=(rnd()%n)+1, r=(rnd()%n)+1, x, y;
        if(l>r)
            swap(l,r);
        if(op==3)
            x=(rnd()%(r-l+1))+1;
        else
            x=(rnd()%vm)+1;
        if(op==4)
            y=(rnd()%vm)+1; // <=vm
        
        if(op==1){
            // add [l,r] + x
            for(auto [it,ed]=split_get(l,r);it!=ed;++it){
                it->v = (it->v + x);// % MOD;
            }
        }else if(op==2){
            // set [l,r] = x
            // 这是降低段数的关键
            auto [it,ed]=split_get(l,r);
            it=odt.erase(it,ed);
            odt.emplace_hint(it,Data{l,r,x});
        }else if(op==3){
            // query [l,r] smallest x
            int tsz=0;
            for(auto [it,ed]=split_get(l,r);it!=ed;++it){
                tmp[tsz++]=pii{it->v,it->r-it->l+1};
            }
            sort(tmp,tmp+tsz);
            int pre=0, ans=0;
            for(int i=0;i<tsz;i++){
                pre+=tmp[i].second;
                if(pre>=x){
                    ans=tmp[i].first; break;
                }
            }
            cout<<ans<<'\n';
        }else{
            // query [l,r] sum a^x % y
            int res=0;
            for(auto [it,ed]=split_get(l,r);it!=ed;++it){
                res = (res + qpow(it->v,x,y)*(it->r-it->l+1)%y) % y;
            }
            cout<<res<<'\n';
        }
    }
}
```