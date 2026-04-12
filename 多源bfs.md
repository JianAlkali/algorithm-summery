[[图论]]

$O\left(n+m\right)$，后续步骤主要在边上两点是不同源的时候进行，这里放入upd中以方便后续按距离处理。
```cpp
    for(int i=0;i<=n;i++){ // 清空
        vif[i]=0;
        vis[i]=INF;
        upd[i].clear();
    }
    queue<int> q;
    for(int i=1;i<=n;i++){
        if(a[i]){ // a[i]==1是源点
            q.emplace(i);
            vis[i]=0;
            vif[i]=i;
        }
    }
    while(!q.empty()){
        int u=q.front(); q.pop();
        for(int i=head[u];i;i=e[i].nxt){
            int v=e[i].v;
            if(vis[v]==INF){
                vis[v]=vis[u]+1;
                vif[v]=vif[u];
                q.emplace(v);
            }else if(vif[v]<vif[u]){ // 使用"<"可以使得每条边只计算一次，优于"!="
                int step=vis[u]+vis[v]+1;
                upd[step].emplace_back(vif[u],vif[v]);
            }
        }
    }
```
