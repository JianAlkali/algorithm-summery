[[_动态规划]]

$O\left(n\right)$找出`s`中是否包含`t`，有哪些位置包含`t`。其中`pi[i]`也代表，在位置`i`上，令`t’`为`t`的前缀即子串`[0,i]`，令`u`为`t’`的`t’`除本身的子串，满足`u`既是`t’`的前缀也是`t’`的后缀的最大u的长度
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
