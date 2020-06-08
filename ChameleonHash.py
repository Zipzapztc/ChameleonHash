import random
from pyunit_prime import get_large_prime_length    #随机生成指定长度大素数
from pyunit_prime import is_prime                  #判断素数
from pyunit_prime import prime_range               #输出指定区间素数
import math


p=0
q=0
    
def primeFactorization(length):                    #分解质因数
    global p,q
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
    return result  

def quickPower(a,b,c):                               #快速幂
    result=1
    while b>0:
        if b%2==1:
            result=result*a%c
        a=a*a%c
        b>>=1
    return result

def getGenerator(result):                             #get g
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

def getSecretKey():                                 #get SK,x
    x=random.randint(1,q)
    return x

def getPublicKey(g,x):                             #get PK,h
    h=quickPower(g,x,p)
    return h

def treatMSG(msg):                                #处理消息msg为整数
    newmsg=''
    for i in msg:
        newmsg+=str(ord(i))
    return int(newmsg)

def ChameleonHash(PK,g,m,r):                       #变色龙哈希
    CH=quickPower(g,m,p)*quickPower(PK,r,p)%p
    return CH

def exgcd(a,b):                                    #扩展欧几里得
    if b==0:
        return 1,0,a
    else:
        x,y,gcd=exgcd(b,a%b)
        x,y=y,(x-(a//b)*y)
        return x,y,gcd

def Forge(SK,m1,r1,m2):                            #求r'
    x,y,gcd=exgcd(SK,q)
    result=x*(m1-m2+SK*r1)%q
    return result

if __name__ == "__main__":
    print('calculating...')
    print('')
    length=100                                    #随机大素数长度
    result=primeFactorization(length)
    g=getGenerator(result)
    SK=getSecretKey()
    PK=getPublicKey(g,SK)
    
    msg1='i sent first message'                  #消息1
    msg2='second message'                        #消息2
    newmsg1=treatMSG(msg1)
    newmsg2=treatMSG(msg2)
    rand1=random.randint(1,q)                    # r

    print('q=',q)
    print('p=',p)
    print('g=',g)
    print('SK=',SK)
    print('PK=',PK)
    print('')

    print('msg1=',msg1)
    print('rand1=',rand1)
    CH=ChameleonHash(PK,g,newmsg1,rand1)
    print('CH=',CH)
    print('')
    
    print('msg2=',msg2)
    rand2=Forge(SK,newmsg1,rand1,newmsg2)
    print('rand2=',rand2)
    newCH=ChameleonHash(PK,g,newmsg2,rand2)
    print('newCH=',newCH)

