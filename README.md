# python_performance
## 前言 (Description)
眾所皆知，Python 不是一個執行效率快的程式語言。  
即便如此，在更了解模組使用與語法選擇，仍可大幅提升執行效率。  

這邊的內容不深入討論演算法；  
而是分享在各種實測下，以效率為優先且更 "Pythonic" 的寫作方式與技巧。  
  
所有內容皆可能因數據大小/結構與Python及系統環境差異而有所差別。  
但在基礎規範中，都可以作為標準依據參考。  
而實戰效能評估則建議仍可利用[效能檢測裝飾器](checkTime.py),[timeit](https://docs.python.org/zh-tw/3/library/timeit.html)或更進階的[bigO](https://github.com/pberkes/big_O),來做為最終評比。





## 1.字串拼接

字串拼接有許多方式，在python 3.6 推出 f-string後，其實就不應該考慮其他拼接方式了。  
因為f-string比其他方式更易讀，且更有效率。  
用 + 的方式雖然省事，在 python 也鮮少出現初學 javascript 時常混淆數值相加還是字串拼接的問題。  
但為了整體的效能與更易讀，還是使用 f-string 吧！  
  
當需要格式化字串可參考[官方文件](https://docs.python.org/zh-tw/3/tutorial/inputoutput.html#formatted-string-literals
)：  

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

python3 -m timeit -s "from string import Template; x = 'f'; y = 'z'; t = Template('$x $y')" "t.substitute(x=x, y=y)"  # template string2
1000000 loops, best of 5: 390 nsec per loop

python3 -m timeit -s "from string import Template; x = 'f'; y = 'z'; t = Template('$x $y').substitute" "t(x=x, y=y)"  # template string3
1000000 loops, best of 5: 388 nsec per loop

python3 -m timeit -s "from string import Template; x = 'f'; y = 'z'" "Template('$x $y').substitute(x=x, y=y)"  # template string
500000 loops, best of 5: 545 nsec per loop
```

## 2.字串列表拼接
當需要拼接 list/tuple/set 等可循環的資料，最快的方式是 ```''.join()``` 

必須留意的是，使用```''.join()```時資料必須是```str```，因此需要先將資料轉為```str```格式。
我們也可以利用map方式來將非```str```格式的資料轉換為```str```格式，  
如：
```''.join(map(str,iterList))```

```shell
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


print(a(strList)),print(b(strList))
#[0.06821919s] a([['0', '1', '2'], ['3', '4', '5'], ['6', '7', '8'], ['9', '10', '11', '12']]) -> 0123456789101112
#[1.68363976s] b([['0', '1', '2'], ['3', '4', '5'], ['6', '7', '8'], ['9', '10', '11', '12']]) -> 0123456789101112
```
另外 dict in list該如何處理呢？
```python
strList = {1:['0', '1', '2'], 2:['3', '4', '5'], 3:['6', '7', '8'], 4:['9', '10', '11', '12']}

@checkTimer
def a(strList):
    for _ in range(1000000):
        s = ''.join(map(lambda x:''.join(strList[x]),strList))
@checkTimer
def b(strList):
    for _ in range(1000000):
        s = ''.join(map(lambda x:''.join(x[1]),strList.items()))

a(strList),b(strList)
#[3.76131233s] a({1: ['0', '1', '2'], 2: ['3', '4', '5'], 3: ['6', '7', '8'], 4: ['9', '10', '11', '12']}) -> None
#[3.74213033s] b({1: ['0', '1', '2'], 2: ['3', '4', '5'], 3: ['6', '7', '8'], 4: ['9', '10', '11', '12']}) -> None
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
根據Python[官方文件](https://docs.python.org/zh-tw/3/reference/simple_stmts.html#augmented-assignment-statements)說明：  
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

a(),b()
#[0.02506243s] a() -> None
#[0.01312026s] b() -> None
```
## 4. 合併列表(後加總)
透過```from itertools import chain```是可最合併多個list的方式。  
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
但當你的需要合併的列表數低於5組的情況下，  
你應該選擇的方式是利用 ```+``` 而非 ```chain```。  
參考下表，10 組的列表，在取其中 5 組的時候 ```chain``` 效率會開始高於 ```+```。
```python
from itertools import chain

lis = [[1, 2, 3, 4, 5] for _ in range(10)]

@checkTimer
def a():
    for _ in range(10000):
        s = sum(chain.from_iterable(lis))
    return s


@checkTimer
def b():
    for _ in range(10000):
        s = sum(lis[0] + lis[1] + lis[2] + lis[3] + lis[4] + lis[5] + lis[6] +
                lis[7] + lis[8] + lis[9])
    return s


@checkTimer
def c():
    for _ in range(10000):
        s = sum(chain.from_iterable(lis[:6]))
    return s


@checkTimer
def d():
    for _ in range(10000):
        s = sum(lis[0] + lis[1] + lis[2] + lis[3] + lis[4] + lis[5])
    return s


@checkTimer
def e():
    for _ in range(10000):
        s = sum(chain.from_iterable(lis[:2]))
    return s


@checkTimer
def f():
    for _ in range(10000):
        s = sum(lis[0] + lis[1])
    return s


a(), b(), c(), d(), e(), f()
#[0.00892185s] a() -> 150
#[0.01682082s] b() -> 150
#[0.00752668s] c() -> 90
#[0.00900056s] d() -> 90
#[0.00506019s] e() -> 30
#[0.00341914s] f() -> 30
```

## 5.時間複雜度
[參考資料](https://gist.github.com/Gr1N/60b346b5e91babb5efac)  

### list
| 操作 |Operation     | Example      | Class         | Notes
|  :----:  |  :----:  | :----:  |  :----:  | :----:  |
| 索引 |Index         | l[i]         | O(1)	     | |
| 存放 |Store         | l[i] = 0     | O(1)	     | |
| 長度 |Length        | len(l)       | O(1)	     | |
| 添加 |Append        | l.append(5)  | O(1)	     | |
| 取出 |Pop	      | l.pop()      | O(1)	     | same as l.pop(-1), popping at end |
| 清除 |Clear         | l.clear()    | O(1)	     | similar to l = [] |
| 分割 |Slice         | l[a:b]       | O(b-a)	     | l[1:5]:O(l)/l[:]:O(len(l)-0)=O(N) |
| 展開 |Extend        | l.extend(...)| O(len(...))   | depends only on len of extension |
| 轉換 |Construction  | list(...)    | O(len(...))   | depends on length of argument |
| 比較 |check ==, !=  | l1 == l2     | O(N)          | |
| 插入 |Insert        | l[a:b] = ... | O(N)	     | |
| 刪除 |Delete        | del l[i]     | O(N)	     |  |
| 移除 |Remove        | l.remove(...)| O(N)	     |  |
| 包含 |Containment   | x in/not in l| O(N)	     | searches list |
| 複製 |Copy          | l.copy()     | O(N)	     | Same as l[:] which is O(N) |
| 取出 |Pop	      | l.pop(0)     | O(N)	     |  |
| 取最大/最小 |Extreme value | min(l)/max(l)| O(N)	     | |
| 反轉 |Reverse	      | l.reverse()  | O(N)	     | |
| 遞迴 |Iteration     | for v in l:  | O(N)          | |
| 排序 |Sort          | l.sort()     | O(N Log N)    | key/reverse doesn't change this |
| 多重遞迴 |Multiply      | k*l          | O(k N)        | 5*l is O(N): len(l)*l is O(N**2) |

```tuple()``` 與列表擁有相同的時間複雜度，差異性在於，tuple無法執行增加與刪除操作，但相同資料節省更多的空間。  
此外創建() ```list()``` 耗時會相較 ```tuple``` 來得短。
```python
lis = [[1, 2, 3, 4, 5] for _ in range(10)]

@checkTimer
def a():
    for _ in range(10000):
        s = tuple(chain.from_iterable(lis))
    return 


@checkTimer
def b():
    for _ in range(10000):
        s = list(chain.from_iterable(lis))
    return 
a(), b()
#[0.01175988s] a() -> None
#[0.01078576s] b() -> None
```
### set
| 操作 | Operation     | Example      | Class         | Notes |
| :--------------: | :--------------: | :--------------: | :---------------: | :-------------------------------: |
| 長度 | Length        | len(s)       | O(1)	     | |
| 添加 | Add           | s.add(5)     | O(1)	     | |
| 包含 | Containment   | x in/not in s| O(1)	     | compare to list/tuple - O(N) |
| 移除 | Remove        | s.remove(5)  | O(1)	     | compare to list/tuple - O(N) |
| 拋棄 | Discard       | s.discard(5) | O(1)	     |  |
| 取出 | Pop           | s.pop()      | O(1)	     | compare to list - O(N) |
| 清除 | Clear         | s.clear()    | O(1)	     | similar to s = set() |
| 轉換 | Construction  | set(...)     | len(...)      | |
| 比較 | check ==, !=  | s != t       | O(min(len(s),lent(t)) |
| 左移位運算 | <=/<          | s <= t       | O(len(s1))    | issubset |
| 右移位運算 | >=/>          | s >= t       | O(len(s2))    | issuperset s <= t == t >= s |
| 集合 | Union         | s | t        | O(len(s)+len(t)) |
| 交集 | Intersection  | s & t        | O(min(len(s),lent(t)) |
| 差集 | Difference    | s - t        | O(len(t))     | |
| 對稱差集 | Symmetric Diff| s ^ t        | O(len(s))     | |
| 遞迴 | Iteration     | for v in s:  | O(N)          | |
| 複製 | Copy          | s.copy()     | O(N)	     | |  

```set``` 相較 ```list/tuple```：   
```set```內的資料都是唯一性的，因著透過 ```hash``` 唯一性，  
對尋找內含資料```1 in s```或依值刪除資料```s.remove/discard```時都是 O(1)。  
但資料屬於無序結構，也就是無索引功能，也因此內含無法使用類似list[1]的底標索引找資料。  
  
其中關於從 set 移除特定資料的這三項功能較為相近，因此特別提及：
Remove: 當值不存在 ```set``` 將引發 ```KeyError``` 錯誤，不會返回刪除資料。 (與```list.remove()```相同) 
Discard: 當值不存在 ```set``` “不會“ 引發 ```KeyError``` 錯誤，不會返回刪除資料。
Pop: 當值不存在 ```set``` 將引發 ```KeyError``` 錯誤，會返回取出資料。 (與```list.pop()```相同)  
  
```frozenset()``` 則是 ```set``` 的版本的 ```tuple()```，擁有無法修改的特色。

## Dictionaries
|操作|Operation     | Example      | Class         | Notes
|:--------------:|:--------------:|:--------------:|:--------------:|:--------------:|
|索引|Index         | d[k]         | O(1)	     ||
|儲存|Store         | d[k] = v     | O(1)	     ||
|長度|Length        | len(d)       | O(1)	     ||
|刪除|Delete        | del d[k]     | O(1)	     ||
|取值/設值|get/setdefault| d.method     | O(1)	     ||
|取出值|Pop           | d.pop(k)     | O(1)	     ||
|取物件|Pop item      | d.popitem()  | O(1)	     ||
|清除|Clear         | d.clear()    | O(1)	     | similar to s = {} or = dict()|
|取所有索引|Views         | d.keys()     | O(1)	     ||
|轉換|Construction  | dict(...)    | len(...)      ||
|遞迴|Iteration     | for k in d:  | O(N)          | all forms: keys, values, items|

```dict``` 可稱為擁有索引的 ```set()```，其綜合了 ```set``` 與 ```list``` 許多的優點。  
其缺點就是創建所需的空間較高，但用空間換得的時間，也是相同的巨大。  
我們常見從```json```取出的資料結構進到 Python 後就是一種標準的字典。  
```from collection import defaultdict``` 是一種可以給予預設值的數據結構。
參考下方可以理解使用案例：

若當想將列表中的 ```dict```資料取出並加總，  
如果用 case1 將引發 KeyError，  
若不想出現錯誤，則可能會使用 ```try ... except```。  
但其實你有更好的選擇，採用 case 2 的```defaultdict()```的方式。  
```
data = [{'money': 10, 'name': 'Ken'}, 
        {'money': 50, 'name': 'Sam'},
        {'money': 70, 'name': 'Ken'},
        {'money': 10, 'name': 'Sam'}]

#case 1
dictData = {}
for i in data:
    dictData[i['name']] += i['money']
# 發生例外狀況: KeyError
# 'Ken'

#case 2
from collections import defaultdict
dictData = defaultdict(int)
for i in data:
    dictData[i['name']] += i['money']
print(dictData)
# defaultdict(<class 'int'>, {'Ken': 80, 'Sam': 60})
```
