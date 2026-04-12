[[数论]]

简称CRT。前置：[[exgcd]]。
求解x，有一组方程$x=a_{1}\left(mod m_{1}\right), x=a_{2}\left(mod m_{2}\right), x=a_{3}\left(mod m_{3}\right),$
设$k=\sum_{}^{} a_{i}$，$r_{i}=\frac{k}{m_{i}}$，$r_{i}^{-1}=\frac{1}{r_{i}}\left(mod m_{i}\right)$，则该唯一解x为

$$
x=\sum_{i=0}^{n-1} r_{i}⋅r_{i}^{-1}⋅a_{i} \left(mod k\right)
$$

实现代码：（注意exgcd的实现也要用$i128$）
```cpp
i128 CRT(int n,int a[N],int m[N]){ // res=a_i(mod m_i)
    i128 res=0, k=1;
    for(int i=0;i<n;i++)
        k*=m[i];
    for(int i=0;i<n;i++){
        i128 r=k/m[i], x,y;
        exgcd(r,m[i],x,y); // 求r*x=1(mod a[i])
        res = (res + r * x * a[i] % k) % k;
    }
    return (res%k+k)%k;
}
```
