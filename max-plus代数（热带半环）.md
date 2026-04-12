[[数论]]

是一种代数系统，有$+ ×$操作（下称此代数下的加乘为$⊕ ⊗$
$a⊕b=max\left(a,b\right)$，$a ⊗b =a+b$，零元素=$-∞$，单位元素=0。
如果一个算式的转移满足这种形式（如算节点n很少的图，很大的r轮后的最长路径），则可用该代数意义下的矩阵快速幂优化$O\left(n^{2}⋅r\right)→O\left(n^{3}⋅logr\right)$。
一个事实是图论floyd其实是min-plus（$a⊕b=min\left(a,b\right)$，$a⊗b =a+b$）。
```cpp
using Mat=array<array<int,M>,M>;
Mat add(Mat& a,Mat& b,int m=M){ // r=a+b (m*m矩阵)
    Mat r={};
    for(int i=0;i<m;i++)
        for(int j=0;j<m;j++)
            r[i][j]=max(a[i][j],b[i][j]);
    return r;
}
Mat mul(Mat& a,Mat& b,int m=M){ // r=a*b (m*m矩阵)
    Mat r={};
    for(int k=0;k<m;k++){
        for(int i=0;i<m;i++){
            int tmp=a[i][k]; // 缓存优化
            for(int j=0;j<m;j++){
                r[i][j]=max(r[i][j],tmp+b[k][j]);
            }
        }
    }
    return r;
}
Mat qpow(const Mat& a,int b,int m=M){ // r=a^b (m*m矩阵)
    Mat r={}, tmp=a;
    while(true){
        if(b&1) r=mul(r,tmp,m);
        b>>=1;
        if(!b) break;
        tmp=mul(tmp,tmp,m); // 放在这可优化，少乘一次
    }
    return r;
}
```
