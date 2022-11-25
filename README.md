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
兩者相差時間約是三倍。

 
```python
strList = [['0', '1', '2'], ['3', '4', '5'], ['6', '7', '8'], ['9', '10', '11', '12']]


@checkTimer
def a(strList):
    for _ in range(100000):
        q = ''.join(''.join(i) for i in strList)
    return q

@checkTimer
def b(strList):
    for _ in range(100000):
        q = ''.join(map(''.join,strList))
    return q

print(a(strList))
#[1.68363976s] a([['0', '1', '2'], ['3', '4', '5'], ['6', '7', '8'], ['9', '10', '11', '12']]) -> 0123456789101112
print(b(strList))
#[0.06821919s] b([['0', '1', '2'], ['3', '4', '5'], ['6', '7', '8'], ['9', '10', '11', '12']]) -> 0123456789101112
```

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
