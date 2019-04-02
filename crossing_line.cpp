#include<cstdio>
#define max(a,b)(a>b?a:b)
#define min(a,b)(a>b?b:a)

'''
    大M布置给小M一个题目：首先给出n个在横坐标上的点，然后连续的用半圆连接他们：
    首先连接第一个点与第二点(以第一个点和第二点作为半圆的直径)。然后连接第二个第三个点，直到第n个点。
    现在需要判定这些半圆是否相交了，在端点处相交不算半圆相交。
'''

int main(){
    int t=0;
    scanf("%d",&t);
    while(t>0){
        int num=0;
        scanf("%d",&num);
        int line[1000][2];
        int i=0;
        int st=0,ed=-1000000;
        scanf("%d",&st);
        while(i+1<num){
            if(ed!=-1000000){
                st=ed;
            }
            scanf("%d",&ed);
            line[i][0]=min(st,ed);
            line[i][1]=max(st,ed);
            i++;
        }
        int flag=0;
        for(int i=1;i<num;i++){
            for(int j=0;j<i;j++){
                if(line[i][0]<=line[j][0]){
                    if(line[i][1]>=line[j][0]){
                        continue;
                    }else{
                        flag=-1;
                        break;
                    }
                }else{
                    if(line[i][1]<=line[j][1]){
                        continue;
                    }else{
                        flag=-1;
                        break;
                    }
                }
            }
            if(flag==-1) break;
        }
        if(flag==0) printf("n\n");
        else printf("y\n");
        t--;
    }
    return 0;
}
