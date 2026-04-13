[[_数论]]

迭代形式 $O\left(n\log n\right)$：
和其功能几乎相同的：[[NTT快速数论变换]]
```cpp
const double PI=acos(-1.0);
using Complex=complex<double>;
inl void FFT(vector<Complex>& c, bool inv){
    int n=c.size();
    for(int i=1, j=0, bit; i<n; i++){ // 位反转置换
        bit=n>>1;
        while(j&bit){
            j^=bit; bit>>=1;
        }
        j^=bit;
        if(i<j) swap(c[i],c[j]);
    }
    for(int len=2;len<=n;len<<=1){ // 蝴蝶变换
        int half=len>>1;
        double angle=2*PI/len*(inv?-1:1);
        Complex wn(cos(angle),sin(angle));
        for(int j=0;j<n;j+=len){
            Complex w(1);
            for(int k=j;k<j+half;k++){
                auto tmp=c[k+half]*w;
                c[k+half]=c[k]-tmp;
                c[k]=c[k]+tmp;
                w*=wn;
            }
        }
    }
    if(inv){ // 求逆
        for(int i=0;i<n;i++)
            c[i]/=n;
    }
}
```

## 调用其进行大数乘法
（将进位和去除前导零注释掉即为多项式乘法）：
（进行大数乘法时支持压位，精度在大数位数较大时仍能保持）
```cpp
static vector<Complex> c1,c2; // 用static复用空间
inl void mul(const vector<int>& a,const vector<int>& b, vector<int>& res){
    int alen=a.size(), blen=b.size(), clen=1;
    while(clen < alen+blen) clen<<=1;
    res.resize(clen); c1.resize(clen); c2.resize(clen);
    for(int i=0;i<alen;i++)
        c1[i]=Complex{(double)a[i],0.};
    for(int i=alen;i<clen;i++)
        c1[i]=Complex{0.,0.}; // resize没有全部元素赋0的功能
    for(int i=0;i<blen;i++)
        c2[i]=Complex{(double)b[i],0.};
    for(int i=blen;i<clen;i++)
        c2[i]=Complex{0.,0.};
    FFT(c1,false);
    FFT(c2,false);
    for(int i=0;i<clen;i++) c1[i]*=c2[i];
    FFT(c1,true);
    for(int i=0;i<clen;i++)
        res[i]=round(c1[i].real()); // 取实部 四舍五入
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
