[[_图论]]

计算有负权的全源最短路。复杂度$O\left(n⋅\left(n+m\right)⋅\log n\right)$，可以看出它**在稀疏图上比`floyd`优秀**（$E≈V$复杂度约为$O\left(n^{2}⋅\log n\right)$）（**稠密图上则不如`floyd`**）。
```cpp
struct E{ // 原始边
    int u,v,w;
}e[M+N];
int head[N],ec=0;
void add(int u,int v,int w){
    e[++ec]={u,v,w};
}
struct En{ // 新边（均加n(new)后缀
    int v,w,nxt;
}en[M];
int headn[N],ecn=0;
void addn(int u,int v,int w){
    en[++ecn]={v,w,headn[u]};
    headn[u]=ecn;
}
int h[N]; // 势
int bst[N][N]; // 结果邻接表u->v
void solve(){
    int n,m;
    cin>>n>>m;
ec=ecn=0;
    for(int i=0;i<=n;i++){
        head[i]=headn[i]=0;
        h[i]=INF;
        fill(bst[i],bst[i]+n+1,INF);
} h[0]=0;
    for(int i=0,u,v,w;i<m;i++){
        cin>>u>>v>>w;
        add(u,v,w);
}
    for(int v=1;v<=n;v++)
        add(0,v,0);

    // 1 bellman-ford O(VE)
    for(int i=0;i<n;i++){
        for(int i=1;i<=ec;i++){
            auto [u,v,w]=e[i];
            if(h[u]+w<h[v]){
                h[v]=h[u]+w;
            }
        }
    }
    for(int i=1;i<=ec;i++){
        auto [u,v,w]=e[i];
        if(h[v]>h[u]+w){ // 第n轮仍可松弛：存在负环
            cout<<-1<<'\n'; return;
        }
    }
    for(int i=1;i<=m;i++){ // 2 建new graph
        auto [u,v,w]=e[i];
        w=w+h[u]-h[v]; // 构建
        addn(u,v,w);
    }
    // 3 dijkstra O(V(V+E)logV)
    priority_queue<pii,vector<pii>,greater<>> pq;
    for(int s=1;s<=n;s++){
        bst[s][s]=0; pq.emplace(0,s);
        while(!pq.empty()){
            auto [co,u]=pq.top(); pq.pop();
            if(co>bst[s][u]) continue;
            for(int i=headn[u];i;i=en[i].nxt){
                int v=en[i].v, w=en[i].w;
                if(co+w<bst[s][v]){ // 注意哪些地方是s，哪些是u
                    bst[s][v]=co+w;
                    pq.emplace(bst[s][v],v);
                }
            }
        } 
        for(int v=1;v<=n;v++) // 4 还原
            if(bst[s][v]!=INF) // wtf不加就错?
                bst[s][v]=bst[s][v]-h[s]+h[v];
	}
```
