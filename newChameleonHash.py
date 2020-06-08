# n个用户，n个PK,SK,r，CH=g^m*h1^r1*h2^r2……hn^rn mod p

#Setup(),KeyGen(),ChameleonHash(),Forge()四个函数
   
import random
from pyunit_prime import get_large_prime_length    #随机生成指定长度大素数
from pyunit_prime import is_prime                  #判断素数
from pyunit_prime import prime_range               #输出指定区间素数
import math


#p=0
#q=0
    
def primeFactorization(length):                    #分解质因数
    #global p,q
    p,q=0,0
    q=get_large_prime_length(length)
    while True:
        d=random.randint(2,10000)
        if d%2==0:
            p=q*d+1
            if is_prime(p)==True:
                break
            else:
                continue
        else:
            continue
    primeList=prime_range(2,int(math.sqrt(d)))
    result=[[0,0] for i in range(len(primeList))]
    for i in range(len(primeList)):
        result[i][0]=primeList[i]
        while d%primeList[i]==0:
            result[i][1]+=1
            d=d//primeList[i]
    if d!=1:
        result.append([d,1])
    result.append([q,1])
    return result,p,q  

def quickPower(a,b,c):                               #快速幂，a^b mod c
    result=1
    while b>0:
        if b%2==1:
            result=result*a%c
        a=a*a%c
        b>>=1
    return result

def getGenerator(result,p,q):                             #get g
    generator=random.randint(1,1000)
    while True:
        if quickPower(generator,q,p)!=1:
            generator+=1
        else:
            for i in range(len(result)):
                if quickPower(generator,int((p-1)/result[i][0]),p)==1:
                    break
            if i!=len(result)-1:
                generator+=1
            else:
                break
    return generator

def Setup(length):
    factorization,p,q=primeFactorization(length)
    g=getGenerator(factorization,p,q)
    return p,q,g

def getSecretKey(n,q):                                 #get SKlist,x1,x2……xn
    SKlist=[]
    for _ in range(n):
        SKlist.append(random.randint(1,q))
    return SKlist

def getPublicKey(g,SKlist,n,p):                        #get PKlist,h1,h2……hn
    PKlist=[]
    for i in range(n):
        PKlist.append(quickPower(g,SKlist[i],p))
    return PKlist

def KeyGen(p,q,g,n):
    SKlist=getSecretKey(n,q)
    PKlist=getPublicKey(g,SKlist,n,p)
    return SKlist,PKlist
    
def getr(n,q):                                         # rlist,r1,r2……rn
    rlist=[]
    for _ in range(n):
        rlist.append(random.randint(1,q))
    return rlist

def treatMSG(msg):                                #处理消息msg为整数
    newmsg=''
    for i in msg:
        newmsg+=str(ord(i))
    return int(newmsg)

def ChameleonHash(PKlist,m,rlist,p,q,g,n):                 #变色龙哈希
    newm=treatMSG(m)
    CH=quickPower(g,newm,p)
    for i in range(n):
        CH=CH*quickPower(PKlist[i],rlist[i],p)
    CH=CH%p
    return CH
    
def exgcd(a,b):                                    #扩展欧几里得
    if b==0:
        return 1,0,a
    else:
        x,y,gcd=exgcd(b,a%b)
        x,y=y,(x-(a//b)*y)
        return x,y,gcd

def Forge(SKlist,m1,rlist,m2,p,q,g,n,i):                            #求r',线性同余方程
    newm1=treatMSG(m1)
    newm2=treatMSG(m2)
    x,y,gcd=exgcd(SKlist[i-1],q)
    result=x*(newm1-newm2+SKlist[i-1]*rlist[i-1])%q
    return result

if __name__ == "__main__":
    print('calculating...')
    print('')
    length=40                                    #随机大素数的长度
    n=5                                           # 用户数为n
    p,q,g=Setup(length)
    SKlist,PKlist=KeyGen(p,q,g,n)
    rlist=getr(n,q)
    
    msg1='i sent first message'                  #消息1
    msg2='second message'                        #消息2

    #print('q=',q)
    #print('p=',p)
    #print('g=',g)
    #print('SK=',SKlist)
    #print('PK=',PKlist)
    #print('')

    print('msg1=',msg1)
    #print('r=',rlist)
    CH=ChameleonHash(PKlist,msg1,rlist,p,q,g,n)
    print('CH=',CH)
    print('')

    i=2                                         #第i个用户改变消息
    print('msg2=',msg2)
    rand2=Forge(SKlist,msg1,rlist,msg2,p,q,g,n,i)
    #print('rand2=',rand2)
    rlist[i-1]=rand2
    newCH=ChameleonHash(PKlist,msg2,rlist,p,q,g,n)
    print('newCH=',newCH)

