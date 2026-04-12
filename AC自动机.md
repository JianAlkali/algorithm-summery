[[动态规划]]

AC自动机是KMP+Trie树的结合体。它相当于允许多个模版串的KMP。复杂度：$O\left(S+\sum_{}^{} T_{i}\right)$。其有统计位置和不统计位置的写法。统计位置并不会增加内部复杂度，但最坏情况下输出的pos数量会达到平方级，当然OJ卡这个是不可能的，否则直接打表都过不了。
不统计位置的写法：
```cpp
const int LOW=-'a', HI=-'A'+26, DIG=-'0'+26+26, C=26+26+10;
struct AC{
    struct Nd{
        array<int,C> nxt; // 可改map写法：内存小些,常数大些
        int fail;
        vi prefail; // 反向fail
        int edid;
    } t[N] {{},0,{},0};
    vi id2str[N];
    int tcnt=0, idcnt=0, scnt=0; //t -edid-> id -id2str-> str
    int _hash(char c){ // 字串->idx 如果只有小写直接返回c-'a'
        if(islower(c))
            return c+LOW;
        else if(isupper(c))
            return c+HI;
        else
            return c+DIG;
    }
    void clear(){
        for(int i=0;i<=tcnt;i++)
            t[i] = {{},0,{},0};
        for(int i=0;i<=idcnt;i++)
            id2str[i].clear();
        tcnt=idcnt=scnt=0;
    }
```

```cpp
    void add(const string& s){
        int now=0, n=s.size();
        for(int i=0;i<n;i++){
            int c=_hash(s[i]);
            if(!t[now].nxt[c]) t[now].nxt[c]=++tcnt;
            now = t[now].nxt[c];
        }
        if(!t[now].edid)
            t[now].edid=++idcnt;
        id2str[t[now].edid].emplace_back(++scnt);
    }
    void build(){ // 构建fail链
        queue<int> q;
        for(int i=0;i<C;i++){
            if(t[0].nxt[i])
                q.emplace(t[0].nxt[i]);
        }
        while(!q.empty()){
            int u=q.front(); q.pop();
            int v=t[u].fail;
            for(int i=0;i<C;i++){
                if(!t[u].nxt[i]){
					 // u->nxt 直接是 v->nxt
                    t[u].nxt[i]=t[v].nxt[i];
                }else{
					 // u->nxt的fail 是 v->nxt
                    t[t[u].nxt[i]].fail = t[v].nxt[i];
                    t[t[v].nxt[i]].prefail.emplace_back(t[u].nxt[i]);
                    q.emplace(t[u].nxt[i]);
                }
            }
        }
}
```

```cpp
    vi query(const string& s){
        vi tres(tcnt+1), idres(idcnt+1), res(scnt+1); // 1based
        int now=0;
        int n=s.size();
        for(int i=0;i<n;i++){
            int c=_hash(s[i]);
            now=t[now].nxt[c];
            tres[now]++;
        }
        // dfs tres->idres
        auto dfs=[&](auto&& dfs,int u)->int {
            int aft=tres[u];
            for(int pf:t[u].prefail){
                aft += dfs(dfs,pf);
            }
            if(t[u].edid) idres[t[u].edid]=aft;
            // cout<<u _ aft _ t[u].edid _ '\n';
            return aft;
        };
        for(int i=0;i<C;i++){
            if(t[0].nxt[i])
                dfs(dfs,t[0].nxt[i]);
        }
        // 还原 idres->res 如果题目保证模版串两两不同可直return id
        for(int i=1;i<=idcnt;i++){
            if(idres[i]){
                for(int strid:id2str[i]){
                    res[strid]=idres[i];
                }
            }
        }
        return res;
    }
} ac;
```
