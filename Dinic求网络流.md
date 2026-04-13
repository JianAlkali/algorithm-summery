[[_图论]]

复杂度$O\left(n^{2}+m\right)$
```cpp
struct Dinic{
    struct E{
        int v,w,nxt;
    }edge[M>>1]; //链式前向星
    int ecnt=1, head[N];
    array<int,N> cur; //当前弧优化
    array<int,N> lv; //分层图
    int to; //汇点（这里默认求的是1->to网络流）
    bool bfs(){
        fill(all(lv,to+1),0);
        queue<int> q;
        q.push(1); lv[1]=1;
        while(!q.empty()){
            int u=q.front(); q.pop();
            for(int eg=head[u];eg;eg=edge[eg].nxt){  
                auto [v,w,_]=edge[eg];
                if(w && !lv[v]){ //有剩余流量&未分层，则可以走此增流
                    q.emplace(v);
                    lv[v]=lv[u]+1;
                }
            }
        }
        return lv[to]; //如果连汇点都到不了的话，就不可能增流了
    }
    int dfs(int u,int fl){
        if(u==to) return fl;
        for(int& eg=cur[u];eg;eg=edge[eg].nxt){ // 注意加引用 
            auto [v,w,_]=edge[eg];
            if(lv[u]+1==lv[v] && w){
                int d=dfs(v,min(w,fl));
                edge[eg].w-=d;
                edge[eg^1].w+=d; //反向边增流
                return d;
            }
        }
        return 0;
    }
```

```cpp
    void _add(int u,int v,int w){ //内部加边
        edge[ecnt]={v,w,head[u]};
        head[u]=ecnt++;
    }
// 外部接口：
void add(int u,int v,int w){
        _add(u,v,w);
        _add(v,u,w);
    }
    int ans(){
        int ans=0;
        while(bfs()){ //可以找到增流路，便dfs
            copy(all(head,to+1),cur.begin()); //重置弧优化
            while(int add=dfs(1,INF)){ //逐步拿取当前分层图的所有流量
                ans+=add;
            }
        }
        return ans;
    }
    Dinic(int n){
        to=n;
        fill(all(head,n+1),0); 
        ecnt=1;
    }
};
```
