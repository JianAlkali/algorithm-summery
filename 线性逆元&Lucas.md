[[_数论]]

$O\left(M+\log MOD\right)$：
`lucas_Cnm`是对于$C_{n}^{m}$的`n`、`m`大于模数的时候的使用方案，此时`Cnm`失效。
```cpp
array<int,MOD> fa,vfa;
inl void init(){
    fa[0]=1;
    for(int i=1;i<MOD;i++)
        fa[i]=fa[i-1]*i%MOD;
    vfa[MOD-1]=qpow(fa[MOD-1],MOD-2);
    for(int i=MOD-1;i>0;i--)
        vfa[i-1]=vfa[i]*i%MOD;
}
inline int Cnm(int n,int m){ //O(1)
    return fa[n]*vfa[n-m]%MOD*vfa[m]%MOD;
}
//将n、m看成MOD进制数，提取他们的每一位进行Cnm，其结果之积即为模MOD意义下的结果
inl int lucas_Cnm(int n,int m){
	if(m==0) return 1;
	return lucas_Cnm(n/MOD,m/MOD) * Cnm(n%MOD,m%MOD) % MOD;
}

inl void mul(vector<int> a,vector<int> b, vector<int>& res){
    int alen=a.size(), blen=b.size(), clen=1;
    while(clen < alen+blen) clen<<=1;
    res.resize(clen); a.resize(clen); b.resize(clen);
    NTT(a,false);
    NTT(b,false);
    for(int i=0;i<clen;i++) res[i]=a[i]*b[i]%MOD;
    NTT(res,true);
    // 进位（clen已经足够大，不会有需要扩容的情况，可以用这种写法）
    for(int i=1;i<clen;i++){
        res[i]+=res[i-1]/10;
        res[i-1]%=10;
    }
    // 去除前导零，若res为0，res=[0]
    while(res.size()>1 && res.back()==0)
       res.pop_back();
}
```
