[[_数论]]

原理和[[FFT快速傅里叶变换]]类似，虽然没有了`FFT`的较慢的浮点计算，但我在luogu上测试其的时间常数和`FFT`差别不大
```cpp
inl void NTT(vector<int>& c, bool inv){
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
        int wn=qpow(3,(MOD-1)/len); 
        if(inv) wn=qpow(wn,MOD-2);
        for(int j=0;j<n;j+=len){
            int w=1;
            for(int k=j;k<j+half;k++){
                auto tmp=(c[k+half]*w)%MOD;
                c[k+half]=(c[k]-tmp+MOD)%MOD;
                c[k]=(c[k]+tmp)%MOD;
                w=w*wn%MOD;
            }
        }
    }
    if(inv){ // 求逆
        int v=qpow(n,MOD-2);
        for(int i=0;i<n;i++)
            c[i]=c[i]*v%MOD;
    }
}
```

调用其进行大数乘法（将进位和去除前导零注释掉即为多项式乘法）：
（由于不涉及浮点运算，在进位前乘积不超过模数时不会有精度损失（10进制下是完全安全的），但也因此压位时需要注意不能压太多位）