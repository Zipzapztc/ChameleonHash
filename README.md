# ChameleonHash

ChameleonHash.py：原版变色龙哈希，一个用户一组公钥私钥。

newChameleonHash.py：进行了封装，更好理解，支持n个用户n组公钥私钥。

## 变色龙哈希函数实例

* Setup(λ)：输入安全性参数λ，构造满足安全参数λ的大素数p，q，其中p，q满足 p=kq+1，选取乘法循环群Zp中阶为q的元素g，输出公共参数pp=(p,q,g) ；

* KeyGen(pp)：输入公共参数pp，在乘法循环群Zq中随机选择指数x，计算h=g^x。最后得到私钥SK=x，HK=h；

* Hash(HK,m,r)：输入公钥HK=h，消息m，随机数r，其中m，r均为Zq中的元素，输出变色龙哈希值CH=g^m*h^r mod p；

* Forge(CK,m,r,m')：输入私钥CK=x，消息m，随机数r，消息m'，其中m，r，m'均为Zq中的元素，根据CH=g^m*h^r =g^m'*h^r' mod p，可得m+rx=m'+r'x mod q，继而可计算出r'=(m-m'+rx)*x^(-1) mod q。
