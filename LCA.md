[[_图论]]

$\log \left(n\right)$的，带代价（带`cost`的跳还有一种写法：`dist[u]`代表从`u`到根的代价）
```cpp
struct E{
    int v,w,nxt;
}e[N<<1];
int head[N], ecnt=0;
inl void add(int u, int v, int w){
    e[++ecnt]={v,w,head[u]};
    head[u]=ecnt;
}
int fa[N][24], cost[N][24];
int dep[N], lg[N]; // 这里dep从0开始算，即代表上方节点个数
inl void solve(){
    int n, q;
    cin>>n>>q;
    fill(head,head+n+1,0);
    ecnt=0;
    for(int i=1,u,v,w;i<n;i++){
        cin>>u>>v>>w;
        add(u,v,w);
        add(v,u,w);
    }
    auto dfs=[&](auto&& dfs, int u, int f)->void{
        dep[u]=dep[f]+1;
        fa[u][0]=f;
        for(int i=1, ed=lg[dep[u]];i<=ed;i++){
            fa[u][i]=fa[fa[u][i-1]][i-1];
            cost[u][i]=cost[fa[u][i-1]][i-1]+cost[u][i-1];
        }
        for(int i=head[u];i;i=e[i].nxt){
            int v=e[i].v, w=e[i].w;
            if(v==f) continue;
            cost[v][0]=w;
            dfs(dfs,v,u);
        }
    };
    dfs(dfs,1,0);

    auto lca=[&](int x, int y){
        if(dep[x]<dep[y]) swap(x,y); //then dep[x]大
        int res=0, dif=dep[x]-dep[y];
        for(int i=0; dif; i++,dif>>=1){
            if(dif&1){
                res+=cost[x][i];
                x=fa[x][i];
            }
        }
        if(x==y) return pii{x,res};
        for(int i=lg[dep[x]];i>=0;i--){
            if(fa[x][i]!=fa[y][i]){
                res+=cost[x][i]+cost[y][i];
                x=fa[x][i]; y=fa[y][i];
            }
        }
        return pii{fa[x][0],res+cost[x][0]+cost[y][0]};
    };
    for(int i=0,u,v;i<q;i++){
        cin>>u>>v;
        auto [fafa, coco]=lca(u,v);
        cout<<fafa<<' '<<coco<<'\n';
	}
}
```