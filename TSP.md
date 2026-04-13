[[_图论]]

寻找一条代价最小的回路。复杂度$O\left(n^{2}⋅2^{n}\right)$。
此处展示非标准的`TSP`：`n`个点，有点权`val`，有选择点数上限`m`个，求最长路径。
最短路径仅需改`max`为`min`。无点权仅需将所有`val`删掉。无选择点数量上限仅需将`m`改成`n`。
```cpp
constexpr ll K=18;
int dp[(1<<K)][K];
int g[K][K];
int val[K];
#define low(x) ((x)&(-(x)))
#define gos(x) \
    ( ((x)+low(x)) | \
    ((( ((x)+low(x)) ^(x)) >>2 ) /low(x) ) )
void solve(){
    int n,m;
    cin>>n>>m;
    for(int i=0;i<n;i++){
        for(int mask=0,ed=1<<n;mask<ed;mask++){
            dp[mask][i]=-1;
        }
        for(int j=0;j<n;j++){
            dp[i][j]=-1;
        }
        val[i]=0;
    }
    for(int i=0;i<n;i++){
        cin>>val[i];
        dp[1<<i][i]=val[i];
    }
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            cin>>g[i][j];
        }
    }

    for(int cnt=2;cnt<=m;cnt++){ // 枚举点数量
        for(int mask=(1<<cnt)-1, ed=(1<<n); mask<ed; mask=gos(mask)){
            for(int last=0;last<n;last++){ // 枚举最后一个点
                if(!(mask&(1<<last))) continue;
                int premask = mask^(1<<last);
                for(int ppre=0;ppre<n;ppre++){
                    if(!(premask&(1<<ppre))) continue;
                    dp[mask][last]=max(
                        dp[mask][last],
                        dp[premask][ppre]
                        + val[last]
                        + bonus[ppre][last]
                    );
                }
            }
        }
    }
    int ans=0;
    for(int mask=(1<<m)-1, ed=(1<<n); mask<ed; mask=gos(mask)){
        for(int last=0;last<n;last++){
            if(mask&(1<<last)){
                ans=max(ans,dp[mask][last]);
            }
        }
    }
    cout<<ans<<'\n';
}
```
