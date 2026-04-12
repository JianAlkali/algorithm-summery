[[杂项]]

所有东西记得搞完保存。
在桌面右键新建文件夹并进入，右键点在终端打开；在命令行输入code . 即可从vscode打开文件夹；新建.cpp，ctrl+j可呼出终端；
编译A.cpp使用 g++ -std=c++14 -O2 -Wall A.cpp ，若要指定输出的名称可以g++ -std=c++14 -O2 -Wall A.cpp NAME
使用 ./a.out 运行a.out；
使用小键盘↑↓可快速切换到上一条执行的命令，tab自动补全；
将in.txt作为输入，结果到控制台：./a.out < in.txt 其中<可理解为左箭头；
将in.txt作为输入，输出到out.txt：./a.out < in.txt > out.txt；
可准备一个std.txt存放预期输出，然后就可以用diff比较了：diff out.txt std.txt 如果一致，什么都不发生，否则输出差异
将文件内容原封不动输出到控制台 cat out.txt；
每次执行输这么多东西麻烦，所以新建run.sh，里面打：
```cpp
#!/bin/sh
g++ -std=c++14 -O2 -Wall A.cpp Aexe
./Aexe < Ain.txt > Aout.txt
cat Aout.txt
diff Aout.txt Astd.txt
```

同时先使用chmod +x run.sh来载入脚本，之后使用 ./run.sh 运行脚本。
对每道题写一个run.sh，而这些文件间仅仅有几个字母ABC的差异，过于麻烦，所以我们可以用$来匹配：
```cpp
#!/bin/sh
g++ -std=c++14 -O2 -Wall $1.cpp exe
./exe < in.txt > out.txt
cat out.txt
diff out.txt std.txt
```

使用 ./run.sh A 来替换$1为A，其他同理，也可以加$2