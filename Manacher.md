[[_动态规划]]

$O\left(n\right)$判断每个字符的最长回文串。利用已有信息避免重复判断，虽然有`while`，但是右边界只会递增，由此避免最坏情况下的平方级别复杂度。
```cpp
int p[N];
inl void solve(){
    string s;
    cin>>s;
    int n=s.size(), m=n*2+3;
    // precal !#a#b#? 这三个特殊字符要两两不同
    // !和?是为了不用在while的时候加入边界判断，较快
    string t(m,'#');
    t[0]='!'; t[m-1]='?';
    for(int i=0, j=2;i<n;i++, j+=2)
        t[j]=s[i];
    // manacher
    int cen=0, ri=0; //当前最右回文的cen和右边界
    fill(p,p+m,0); //pi表示以i为中心的最长回文半径
    for(int i=2;i<m-1;i++){
        if(i<ri) //在cen的半径范围内的扩展才是安全的
            p[i]=min(ri-i,p[(cen<<1)-i]);
        int newp=p[i]+1;
        while(t[i-newp]==t[i+newp])
            newp++;
        p[i]=newp-1;
        if(i+p[i]>ri){ //采用更右的范围
            cen=i;
            ri=i+p[i];
        }
    }
    int ans=0;
    for(int i=0;i<m;i++)
        ans=max(ans,p[i]);
    cout<<ans<<'\n';
}
```
