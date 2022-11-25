# python_performance
## 前言 (Description)
眾所皆知，python 不是一個執行效率快的語言。
但熟練的 coding skill 會讓你的效率大幅提升。
這邊的內容不討論演算法，而是提供我學習過程中，以效率為優先更接近 "Pythonic" 的寫作方式與技巧。


**所有效能比較表，由上至下快至慢。  




## 1.字串拼接

字串拼接有許多方式，在python 3.6 推出 f-string後，其實就不應該考慮其他拼接方式了。  
因為f-string比其他方式更易讀，且更有效率。  
用 + 的方式雖然省事，在 python 也鮮少出現初學 javascript 時常混淆數值相加還是字串拼接的問題。  
但為了整體的效能與更易讀，還是使用 f-string 吧！  
  
當需要格式化字串可參考官方文件：https://docs.python.org/zh-tw/3/tutorial/inputoutput.html#formatted-string-literals

```bash
python3 -m timeit -s "x = 'f'; y = 'z'" "f'{x} {y}'"  # f-string
5000000 loops, best of 5: 51.1 nsec per loop

python3 -m timeit -s "x = 'f'; y = 'z'" "x + ' ' + y"  # concatenation
5000000 loops, best of 5: 73.2 nsec per loop

python3 -m timeit -s "x = 'f'; y = 'z'" "' '.join((x,y))"  # join
5000000 loops, best of 5: 71.6 nsec per loop

python3 -m timeit -s "x = 'f'; y = 'z'; t = ' '.join" "t((x,y))"  # join2
5000000 loops, best of 5: 66.6 nsec per loop

python3 -m timeit -s "x = 'f'; y = 'z'" "'{} {}'.format(x,y)"  # format
2000000 loops, best of 5: 165 nsec per loop

python3 -m timeit -s "x = 'f'; y = 'z'; t = '{} {}'.format" "t(x,y)"  # format2
2000000 loops, best of 5: 165 nsec per loop

python3 -m timeit -s "from string import Template; x = 'f'; y = 'z'" "Template('$x $y').substitute(x=x, y=y)"  # template string
500000 loops, best of 5: 545 nsec per loop

python3 -m timeit -s "from string import Template; x = 'f'; y = 'z'; t = Template('$x $y')" "t.substitute(x=x, y=y)"  # template string2
1000000 loops, best of 5: 390 nsec per loop

python3 -m timeit -s "from string import Template; x = 'f'; y = 'z'; t = Template('$x $y').substitute" "t(x=x, y=y)"  # template string3
1000000 loops, best of 5: 388 nsec per loop
```

## 2.字串列表拼接
當需要拼接 list/tuple/set 等可循環的資料，最快的方式是 ```''.join()``` 

必須留意的是，使用```''.join()```時資料必須是```str```，因此需要先將資料轉為```str```格式。
我們也可以利用map方式來將非```str```格式的資料轉換為```str```格式，  
如：
```''.join(map(str,iterList))```
```''.join(map(''.join,map(str,

```bash
python3 -m timeit -s "t = [str(i) for i in range(13)]" "' '.join(t)"  # join
2000000 loops, best of 5: 156 nsec per loop

python3 -m timeit -s "a, b, c, d, e, f, g, h, i, j, k, l, m = [str(s) for s in range(13)]" "f'{a} {b} {c} {d} {e} {f} {g} {h} {i} {j} {k} {l} {m}'"  # f-string
1000000 loops, best of 5: 240 nsec per loop

python3 -m timeit -s "t = [str(s) for s in range(13)]" "'{} {} {} {} {} {} {} {} {} {} {} {} {}'.format(*t)"  # format
500000 loops, best of 5: 652 nsec per loop

python3 -m timeit -s "a, b, c, d, e, f, g, h, i, j, k, l, m = [str(s) for s in range(13)]" "a + ' ' + b + ' ' + c + ' ' + d + ' ' + e + ' ' + f + ' ' + g + ' ' + h + ' ' + i + ' ' + j + ' ' + k + ' ' + l + ' ' + m"  # concat
500000 loops, best of 5: 834 nsec per loop

python3 -m timeit -s "from string import Template; a, b, c, d, e, f, g, h, i, j, k, l, m = [str(s) for s in range(13)]" "Template('$a $b $c $d $e $f $g $h $i $j $k $l $m').substitute(a=a, b=b, c=c, d=d, e=e, f=f, g=g, h=h, i=i, j=j, k=k, l=l, m=m)"  # template string
500000 loops, best of 5: 963 nsec per loop
```
做個寫法簡單示範：  
  
  

如果是單行列表，
不需要用 list comphension 方式 -> ```''.join(i for i in strList)```  
而是使用 ''.join(strList)即可。  
```python
strList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
s = ''.join(strList)
```
如果是 多行 列表(list in list)，  
仍然不需要用 list comphension 方式 -> ```''.join([i for i in strList])```  
而是使用 ```''.join(map(''.join,strList))``` 即可。  
兩者相差時間約是 &#x1F538; 24 倍 &#x1F538;。

 
```python
strList = [['0', '1', '2'], ['3', '4', '5'], ['6', '7', '8'], ['9', '10', '11', '12']]

@checkTimer
def a(strList):
    for _ in range(100000):
        q = ''.join(map(''.join,strList))
    return q


@checkTimer
def b(strList):
    for _ in range(100000):
        q = ''.join(''.join(i) for i in strList)
    return q


print(a(strList))
#[0.06821919s] a([['0', '1', '2'], ['3', '4', '5'], ['6', '7', '8'], ['9', '10', '11', '12']]) -> 0123456789101112
print(b(strList))
#[1.68363976s] b([['0', '1', '2'], ['3', '4', '5'], ['6', '7', '8'], ['9', '10', '11', '12']]) -> 0123456789101112
```
另外 dict in list該如何處理呢？
```
strList = {1:['0', '1', '2'], 2:['3', '4', '5'], 3:['6', '7', '8'], 4:['9', '10', '11', '12']}

@checkTimer
def a(strList):
    for _ in range(1000000):
        s = ''.join(map(lambda x:''.join(strList[x]),strList))
@checkTimer
def b(strList):
    for _ in range(1000000):
        s = ''.join(map(lambda x:''.join(x[1]),strList.items()))

a(strList)
[3.76131233s] a({1: ['0', '1', '2'], 2: ['3', '4', '5'], 3: ['6', '7', '8'], 4: ['9', '10', '11', '12']}) -> None
b(strList)
[3.74213033s] b({1: ['0', '1', '2'], 2: ['3', '4', '5'], 3: ['6', '7', '8'], 4: ['9', '10', '11', '12']}) -> None
```
可以看到兩種方式基本上是相同的，挑個喜歡的即可。

反向教材：當資料是多重結構，且非```string```，但仍想拼接成字串時，這時候要避免多重遞迴造成時間的消耗。
```python

intList = {1:[1,2,3,4,5],2:[1,2,3,4,5,6]}

@checkTimer
def a():
    for _ in range(10000):
        s = ''
        for _,v in intList.items():
            for k in v:
                s += str(k)
    return s

@checkTimer
def b():
    for _ in range(10000):
        s = ''
        for _,v in intList.items():
            for k in v:
                s = f'{s}{str(k)}'
    return s

def c():
    for _ in range(10000):
        s = ''
        for _,v in intList.items():
            for k in v:
                s = s+str(v)
    return s

@checkTimer
def d():
    for _ in range(10000):
        s = ''.join(map(''.join,(map(lambda x:(map(str,intList[x])),intList))))
    return s

@checkTimer
def e():
    for _ in range(10000):
        s = ''.join(map(lambda x:''.join(str(i) for i in x[1]),intList.items()))
    return s

a(),b(),c(),d(),e()
#[0.03594051s] a() -> 12345123456
#[0.03897319s] b() -> 12345123456
#[0.04752491s] c() -> 12345123456
#[0.04102941s] d() -> 12345123456
#[0.46192845s] e() -> 12345123456
```
我們透過前面的比較，知道了 ```f-string``` 快於 ```a+b```，  
但 ```+=``` 會再快於 ```f-string```，```+=```與```a+b```是兩個不一樣的型態模式。  
根據官網說明：https://docs.python.org/zh-tw/3/reference/simple_stmts.html#augmented-assignment-statements  
>增强赋值语句例如 x += 1 可以改写为 x = x + 1 获得类似但并非完全等价的效果。  
>在增强赋值的版本中，x 仅会被求值一次。  
>而且，在可能的情况下，实际的运算是 原地 执行的， 
>也就是说并不是创建一个新对象并将其赋值给目标，而是直接修改原对象。

另外在上方案例```d(),e()```反而與前面提到的```map```效率不符。  
原因在於```d(),e()```的結構有多重遞迴的情況。  
仔細看語法可以發現，為了要將值轉為string我們循環了一次轉換後，才再一次循環將字串拼接起來。  
如詞多重嵌套循環的情況下，再快的方式都會使其遞增為倍數，也就是演算法常提到的 ```O(log n)```。  
而 ```a()``` 與 ```b()``` 則只有 ```O(n)``` 相對來的快。  

## 3.列表推導模式 list/dict/tuple comphenshion 與數字加總
當你所需的資料是需要透過遞迴(loop)組成dict/list/tupe時可多利用。
```python
iterations = 100000

@checkTimer
def a():
    myList = []
    for i in range(iterations):
        myList.append(i+1)

@checkTimer        
def b():
    myList = [i+1 for i in range(iterations)]

a()
[0.02506243s] a() -> None
b()
[0.01312026s] b() -> None
```
## 4. 合併列表(後加總)
透過```from itertools import chain```將可快速合併子列表. 
```a(),b()```為拆分後才加總，  
而```c(),d(),e()```則為循環提出每一個子列表加總，最後再加總，  
同上例最後提到部分，又是一個多重嵌套造成的時間消耗。

```python
lis = [[1,2,3,4,5] for _ in range(50)]


@checkTimer
def a():
    from itertools import chain
    for _ in range(10000):
        s = sum(chain.from_iterable(lis))
    return s

@checkTimer
def b():
    from itertools import chain
    for _ in range(10000):
        s = sum(chain(*lis))
    return s

@checkTimer
def c():
    for _ in range(10000):
        s = sum(map(sum, lis))
    return s

@checkTimer
def d():
    for _ in range(10000):
        s = sum(sum(lis, []))
    return s

@checkTimer
def e():
    for _ in range(10000):
        s =sum(sum(x) for x in lis)
    return s
a(),b(),c(),d(),e()
#[0.02996942s] a() -> 750
#[0.03217515s] b() -> 750
#[0.04394276s] c() -> 750
#[0.14855066s] d() -> 750
#[1.53052591s] e() -> 750
```

