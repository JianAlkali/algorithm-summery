[[_图论]]

稀疏图$E≈V$，稠密图$E≈V^{2}$。
- `Dijkstra`: `pq`按点权越小越前存点，贪心。
- `Bellman-Ford`: 类似`Floyd`，但是是对所有边进行`V-1`次松弛。
- `SPFA`: `Bellman-Ford`基础上，只对发生变化的点进行松弛，平均情况会更优。
- `Floyd`: 对所有点进行松弛，枚举中间点。
- `Johnson`: 虚拟节点到所有点建边权值=0，进行`Bellman-Ford`得到每个点$h_{i}$，重赋权$w_{u→ v}^{'}=w_{u→ v}+h_{u}-h_{v}$。对每个点`Dijkstra`，还原距离$d_{u→v}=d_{u→v}^{'}-h_{u}+h_{v}$。