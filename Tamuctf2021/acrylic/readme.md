# Acrylic
This was a simple Rev challenge
## Description
This is an easy challenge. There is a flag that can be printed out from somewhere in this binary. Only one problem: There's a lot of fake flags as well.
### Files provided
[acrylic](https://github.com/TheRealOddCoder/writeups2021/blob/main/Tamuctf2021/acrylic/acrylic)
## Writeup
Running the binary just printed out `look at the code`.
Running strings on the binary gave a lot of strings resembling **gigem{133t_5tring}**
<br/><br/>
![strings](https://github.com/TheRealOddCoder/writeups2021/blob/main/Tamuctf2021/acrylic/Screenshots/acrylic/strings.png)
<br/><br/>
Let's fire up radare2!
<br/><br/>
There was a function named `get_flag()` and `flags`.
Inside get_flag(), there was some calculations going on and then loads a specific location inside *flags*. Performing those calculations would give the flag location since it is a static binary.
<br/><br/>
![get_flag](https://github.com/TheRealOddCoder/writeups2021/blob/main/Tamuctf2021/acrylic/Screenshots/acrylic/get_flag.png)
<br/><br/>

Looks like there is **while-loop** runnning that looks like,
```
var_x = 0x7b   # this is [var_8h]
var_c = 0x0    # this is [var_4h]

# jmp 0x68c is the while loop

while (var_c < 0x7e4){    # cmp dword[var_4h],0x7e3

  #0x64e
  var_x = ((var_x + 1) * var_x) % 0x7f    # imul eax, dword[var_8h]
  var_c +=1                               # add dword[var_4h],1
  
}    #jmp 0x64e (if var_c< 0x7e4)

return flags+(var_x + 0x40)  #flags address is given as 0x201020
```
Running this calculation in python would give the flag address.
The starting address of `flags` is obtained from static analysis from radare2
## Code
```
location_x = 0x7b
count_variable = 0x0
flag_address = 0x201020


while(count_variable < 0x7e4):
    location_x = ((location_x +1) * location_x) % 0x7f
    count_variable += 1

location_x = location_x * 0x40
flag_address += location_x

print(hex(flag_address))
```
The code returns the address 0x202620. So,the string at 0x202620 is the flag.
<br/><br/>
![flag](https://github.com/TheRealOddCoder/writeups2021/blob/main/Tamuctf2021/acrylic/Screenshots/acrylic/Screenshot%20from%202021-04-26%2008-32-01.png)
<br/><br/>
## Flag
`gigem{counteradvise_orbitoides}`
