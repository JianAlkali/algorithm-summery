[[动态规划]]

字典树是也是一种数据结构，经考虑，还是把它和[[KMP]]等一起放在动态规划里。
它是一个种以一种通过树状结构，高效匹配查询串和模版串，以获取查询串匹配的前缀数量或结尾数量的方法。插入$O\left(n\right)$，查询$O\left(n\right)$。
下面给出固定空间大小（无指针）的模版。
```cpp
const int LOW=-'a', UPP=-'A'+26, DIG=-'0'+26+26, C=26+26+10; // 哈希，用于减少所占空间，这里包含大小写字母和数字
struct Trie{
    struct Nd{
        array<int,C> nxt;
        int pre, ed;
    } t[N]{{},0,0};
int tcnt=0;
    int hash(char c){
        if(islower(c)) return c+LOW;
        else if(isupper(c)) return c+UPP;
        else return c+DIG;
}
    void clear(){
        fill(t,t+tcnt+1,Nd{{},0,0});
        tcnt=0;
}
    void add(const string& s){
        int now=0;
        for(char c:s){
            int hac=hash(c);
            if(!t[now].nxt[hac]){
                t[now].nxt[hac]=++tcnt;
            }
            now=t[now].nxt[hac];
            t[now].pre++;
        }
        t[now].ed++;
    }
```

```cpp
    int querypre(const string& s){
        int now=0;
        for(char c:s){
            int hac=hash(c);
            if(!t[now].nxt[hac]) return 0;
            now=t[now].nxt[hac];
        }
        return t[now].pre;
    }
    int queryed(const string& s){
        int now=0;
        for(char c:s){
            int hac=hash(c);
            if(!t[now].nxt[hac]) return 0;
            now=t[now].nxt[hac];
        }
        return t[now].ed;
    }
} trie;
```
