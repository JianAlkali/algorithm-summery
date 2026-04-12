[[动态规划]]

取一些数位dp的例子。数位dp，核心思想是将一个数字按十进制逐位拆解+记忆化搜索，从高位到低位依次枚举每一位可能的取值+维护状态（是否受限、前导零、数位和、模某个数的余数、最后一个数），从而高效统计满足特定条件的数字个数或最优值的方法。
统计$\left[0,a\right]$上$windy$数的个数，$windy$数：不含前导零且相邻两位数字之差至少为 $2$ 的正整数：
```cpp
auto callower=[](int a)->int {
    if(a==0) return 1; // 按定义，0也是windy数
    vector<vvvi> mem(11,vvvi(2,vvi(2,vi(10,-1))));
    vi upp(11);
    int adig=0, tmp=a;
    while(tmp){ // 获取原数的特征
        upp[++adig]=tmp%10;
        tmp/=10;
    }
    // dig: 当前数位，in: 是否在前导零状态，up: 是否到顶受限，pre: 最后一个数
    auto dfs=[&](auto&& dfs,int dig,int in,int up,int pre)->int {
        if(dig==0) return 1;
        if(mem[dig][in][up][pre]!=-1) 
return mem[dig][in][up][pre];
        int res=0;
        for(int i=0;i<10;i++){
            if(up && i>upp[dig]) break; // 到顶受限提前跳出
            if(in && abs(i-pre)<=1) continue; // 不满足相邻约束
            int nin=in||i!=0; // 前导零+当前位非零->非前导零
            int nup=up&&i==upp[dig]; // 受限+当前位未到顶->无受限
            res += dfs(dfs, dig-1, nin, nup, i);
        }
        return mem[dig][in][up][pre]=res;
    };
    return dfs(dfs,adig,false,true,0);
};
```
