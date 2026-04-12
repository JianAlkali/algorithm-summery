[[动态规划]]

$O\left(n\right)$找出s中是否包含t，有哪些位置包含t。其中$pi\left[i\right]$也代表，在位置i上，令t’为t的前缀即子串$\left[0,i\right]$，令u为t’的t’除本身的子串，满足u既是t’的前缀也是t’的后缀的最大u的长度
```cpp
    string s,t;
    cin>>s>>t;
    int n=s.size(), m=t.size();
    vi pi(m);
    // kmp precal
    for(int i=1, j=0;i<m;i++){
        while(j && t[i]!=t[j])
            j=pi[j-1];
        if(t[j]==t[i])
            j++;
        pi[i]=j;
    }
    // kmp check
    vi ans;
    for(int i=0, j=0;i<n;i++){ //i->s, j->t
        while(j && s[i]!=t[j])
            j=pi[j-1];
        if(s[i]==t[j]){
            if(++j==m){
                int beg=i-(m-1)+1; // 最后一个+1是1based
                ans.emplace_back(beg);
                j=pi[j-1]; // 这是为了找多个匹配的，不加会RE
            }
        }
    }
    for(int a:ans){
        cout<<a<<'\n';
    }
```
