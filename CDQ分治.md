[[_数据结构]]
**CDQ分治**是一种数据结构+算法，用以统计多维偏序问题。尤其是二维或三维偏序（更高维时复杂度不占优）。
在统计三维偏序：计算 $\forall i, cnt(i)= \forall j, i_x \ge j_x, i_y \ge j_y, i_z \ge j_z$ 时，复杂度为$O(n\cdot \log(n) \cdot \log(k))$，其中`k`为值域。在统计二维偏序时，复杂度为$O(n\cdot \log(n))$。
下为[P3810 【模板】三维偏序 / 陌上花开 - 洛谷](https://www.luogu.com.cn/problem/P3810)的**CDQ分治**解法。
```cpp
// 第三维偏序的维护：可回溯树状数组
#define low(x) ((x)&(-(x)))
struct Fen{
    int a[N];
    int n;
    vector<pii> back;
    Fen(){
        fill(a,a+N,0);
    }
    void setn(int n_){
        n=n_;
    }
    void reset(){
        for(auto [p,v]:back){
            add(p,-v,false);
        }
        back.clear();
    }
    void add(int p,int v,bool sign=true){
        if(sign)
            back.emplace_back(p,v);
        while(p<=n) a[p]+=v, p+=low(p);
    }
    int query(int p){
        int r=0; while(p) r+=a[p], p-=low(p);
        return r;
    }
} fen;


using vec=array<int,5>; // x,y,z,cnt,id
int ans[N], cnt[N];
vec a[N], tmp[N];

void merge(int l,int r){
    if(l==r) return;
    int m=(l+r)>>1;
    merge(l,m); merge(m+1,r);
    fen.reset();
    int i=l, j=m+1, k=l;
    // 二维归并 + 三维fen
    // 归并统计 统计内部从 [m+1,r] 到 [l,m] 的贡献 不会重
    while(i<=m && j<=r){
        if(a[i][1]<=a[j][1]){
            fen.add(a[i][2],a[i][3]); // 若只有二维，改成precnt+=a[i][3]
            tmp[k++]=a[i++];
        }else{
            ans[a[j][4]]+=fen.query(a[j][2]); // 若只有二维，改成+=precnt
            tmp[k++]=a[j++];
        }
    }
    while(i<=m) tmp[k++]=a[i++];
    while(j<=r){
        ans[a[j][4]]+=fen.query(a[j][2]);
        tmp[k++]=a[j++];
    }
    for(int i=l;i<=r;i++)
        a[i]=tmp[i]; // a sorted -> b sorted
}

void solve(){
    int n,k;
    cin>>n>>k;
    for(int i=1;i<=n;i++)
        cin>>tmp[i][0]>>tmp[i][1]>>tmp[i][2], tmp[i][3]=1, tmp[i][4]=i;
    fen.setn(k);
    
    // 1 dim: sort
    sort(tmp+1,tmp+n+1,[](const vec& l,const vec& r){
        return l[0]!=r[0]?l[0]<r[0] : l[1]!=r[1]?l[1]<r[1]:l[2]<r[2];
    });
    // 处理相同点
    int an=0;
    for(int i=1,j=1;i<=n;i++){
        while(j+1<=n && tmp[i][0]==tmp[j+1][0] && tmp[i][1]==tmp[j+1][1] && tmp[i][2]==tmp[j+1][2])
            j++;
        a[++an] = {tmp[i][0],tmp[i][1],tmp[i][2],j-i+1,an};
        i=j;
    }
    
    // 2 dim: merge, 3dim: fenwick tree
    merge(1,an);
    
    // 计算位置相同的点的贡献
    for(int i=1;i<=an;i++)
        ans[a[i][4]]+=a[i][3]-1;

    for(int i=1;i<=an;i++)
        cnt[ans[a[i][4]]]+=a[i][3];
    for(int i=0;i<n;i++)
        cout<<cnt[i]<<'\n';
}
```