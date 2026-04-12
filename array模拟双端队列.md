[[其他技巧&我的小东西]]

一个方便的小技巧，减小常数。同时，提供deque所不支持的随机访问，这在维护斜率等要用到多个点值的情况下很有用。有begin、end则也支持stl，操作等同于c数组，如 auto it=lower_bound(all(q)-1,tar,greater<>()) 、for(auto& a:q){…}。这里给出<pii>的实现
```cpp
// array模拟允许随机访问的双端队列
struct Deq{
    int q[N<<1]; //头尾各N
    int l=N, r=N-1; //[l,r]
    inl void clear(){ l=N; r=N-1; }
    inl int size(){ return r-l+1; }
    inl bool empty(){ return l>r; }
    inl void pushf(int v){ q[--l]=v; }
    inl void pushb(int v){ q[++r]=v; }
    inl void popf(){ l++; }
    inl void popb(){ r--; }
    inl auto& f(int idx=0){ return q[l+idx]; }
    inl auto& b(int idx=0){ return q[r-idx]; }
    inl auto* begin(){ return &q[l]; } // 可适配stl
    inl auto* end(){ return &q[r+1]; } // 可适配stl
} q;
```
