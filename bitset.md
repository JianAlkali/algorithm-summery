[[数据结构]]

一般来说，复杂度分析时用bitset的操作为用数组的$\frac{1}{ω}$倍，通常$ω=64$。这个提升许多时候是必要的（$n=2e5时 n^{2}=4e10, \left(\frac{n}{ω}\right)^{2}≈1e7因为64^{2}>4e3$）。
由于bitset<N>操作为$O\left(\frac{N}{ω}\right)$而非$O\left(\frac{}{ω}\right)$以更好的做法是使用变长bitset：
```cpp
template<int BN>
inl void solve(int n){
    if(BN<=n){
        return solve<min(N,BN<<1)>(n);
    }
bitset<BN> bs;
//...
}
signed main(){
		//...
        cin>>n;
        solve<1>(n);
    return 0;
}
```

构造：default：全0，ull：64位，string：二进制字符串。
.test(pos)→bool pos位是否为1
.any()→bool 是否有1  .all()→bool 是否全为1   .none()→bool 是否全为0
.count()→int 返回1的个数
.set() 所有位置1   .set(pos) pos位置1
.set(pos,0) .reset(pos) pos位置0   .reset() 所有位置0
.flip() 所有位反转   .flip(pos) pos位取反
.to_ullong()→ull 返回64位无符号
.to_string(zero=’0’,one=’1’) 转换为二进制字符串