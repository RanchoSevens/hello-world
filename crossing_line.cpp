#include<cstdio>
#define max(a,b)(a>b?a:b)
#define min(a,b)(a>b?b:a)

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
