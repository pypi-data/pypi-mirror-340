'''
Gentoricass Programming Language | Gentoricass编程语言
   Built by: Dickily
   Version: 1.5 (Improved!)

Gentoricass is a beginner-friendly programming language based on Python.  
Its intuitive commands simplify coding while retaining Python's power.  
Gentoricass是一种基于Python的初学者友好型编程语言。  
它的直观命令简化了编程，同时保留了Python的强大功能。

## Features | 特点:
1. Interactive Input | 交互式输入 (`gin`)
2. Flexible Output | 灵活的输出 (`gout`)
3. Logical Conditions | 条件控制 (`gif_true_false`, `gif_in`)
4. Loops with Shared Variables | 支持共享变量的循环 (`grepeat`, `gloop`)
5. Break & Skip in Loops | 循环中的Break和Skip (`gstop`, `gskip`)
6. Random Utilities | 随机数支持 (`gran_int`, `gran_choice`)
7. Custom Function Creation | 自定义函数创建 (`gset`, `grun`)
8. Built-In Documentation | 内置文档支持 (`help(gentoricass)`)

---

## Usage | 用法:
Call `help(gentoricass)` to see a list of functions and their explanations.  
调用`help(gentoricass)`可以查看函数列表及其解释。

---

## Version 1.5 Improvements | 版本1.5改进:
1. **Break & Skip Commands in Conditions**:  
   Loops (`grepeat`, `gloop`) now detect `gstop` and `gskip` commands within `gif_true_false()` logic for dynamic flow control.  

2. **Enhanced Loop Handling**:  
   Optimized loop execution with better variable sharing and dynamic error handling.  

3. **Added Random Utilities**:  
   Introduced `gran_int()` for random integers and `gran_choice()` for selecting random items.  

4. **Improved User Experience**:  
   Simplified syntax and increased clarity in dynamic function creation (`gset`, `grun`).  

Explore Gentoricass and unleash your creativity! 🚀  
'''



import time  # Import the time module for delays | 导入time模块用于延时
import math# Import the math module for mathematical functions | 导入math模块用于数学功能
from math import *# Import all math attributes | 导入math模块的所有属性
import asyncio  # Import asyncio for asynchronous tasks | 导入asyncio模块用于异步任务
import random
### Function 1: gin() ###
def gin(word):
    '''
Interactive Input | 交互式输入

gin() prompts the user for input, with support for multi-line prompts using `(nextline)`.
gin() 提示用户输入，并支持使用`(nextline)`进行多行提示。

Arguments | 参数:
- word (str): The prompt message. Use "(nextline)" to add line breaks.
  提示信息，使用`(nextline)`添加换行。

Returns | 返回:
- str: User input | 用户输入。

Example | 示例:
name = gin("What is your name?(nextline)")
gout("Hello,", name)
'''

    if "(nextline)" in word:
        word = word.replace("(nextline)", "\n")  # Replace (nextline) with newlines
    return input(word)


### Function 2: gout() ###
def gout(*word, next="yes"):
    ''''
Flexible Output | 灵活的输出

gout() prints text or variables with support for multi-line output using `(nextline)`.
gout() 将文字或变量打印到控制台，并支持使用`(nextline)`进行多行输出。

Arguments | 参数:
- *word: Messages or variables to print | 要打印的消息或变量。
- next (str): If "yes", adds a newline. If "no", stays on the same line.
  如果是"yes"，添加换行；如果是"no"，保持在同一行。

Example | 示例:
gout("Welcome to Gentoricass!", "(nextline)Enjoy coding.", next="yes")
'''

    for w in word:
        if isinstance(w, str) and "(nextline)" in w:
            w = w.replace("(nextline)", "\n")  # Replace (nextline) for multi-line
        print(w, "", end="")  # Print without automatic newline
    if next == "yes":
        print()


### Function 3: gif_in() ###
def gif_in(what, in_what):
    '''
Substring Check | 子字符串检查

gif_in() checks if one string is a substring of another.
gif_in() 检查一个字符串是否是另一个字符串的子字符串。

Arguments | 参数:
- what (str): The substring to check | 要检查的子字符串。
- in_what (str): The string to search within | 要搜索的字符串。

Returns | 返回:
- str: "True" if found, "False" otherwise | 如果找到返回"True"，否则返回"False"。

Example | 示例:
result = gif_in("Gentoricass", "Welcome to Gentoricass!")
gout("Result:", result)
'''

    return True if what in in_what else False


### Function 4: gwait() ###
def gwait(times):
    '''
Execution Pause | 暂停执行

gwait() pauses program execution for a specified number of seconds.
gwait() 暂停程序执行指定的秒数。

Arguments | 参数:
- times (float): Duration in seconds | 持续时间（秒）。

Example | 示例:
gout("Pausing for 2 seconds...")
gwait(2)
gout("Done!")
'''

    time.sleep(times)  # Pause execution for the given time


### Function 5: gif_true_false() ###
def gif_true_false(arg, true_do, false_do):
    '''
Conditional Execution | 条件执行

gif_true_false() executes commands dynamically based on `True` or `False` conditions.  
It also supports `gstop` and `gskip` for dynamic flow control.

gif_true_false() 根据条件是否为`True`或`False`动态执行命令，同时支持`gstop`和`gskip`用于控制循环流。

Arguments | 参数:
- arg (bool): The condition (`True` or `False`) | 条件 (`True` 或 `False`)。
- true_do (str): Command(s) to execute if `True`. Use `;` to separate multiple commands. | 如果为`True`时执行的命令，用`;`分隔多个命令。
- false_do (str): Command(s) to execute if `False`. Use `;` to separate multiple commands. | 如果为`False`时执行的命令，用`;`分隔多个命令。

Example | 示例:
gif_true_false(True, 'gout("Correct!")', 'gout("Wrong!")')
'''

    if arg==True:
        true_do=true_do.split(";")
        for do in true_do:
            if do == "gstop":
                return "gstop"
            if do== "gskip":
                return "gskip"
            exec(do,globals())
    if arg==False:
        false_do=false_do.split(";")
        for do in false_do:
            exec(do,globals())


### Function 6: grepeat() ###
def grepeat(what, in_what, *do,share=[]):
    '''
For Loop Execution | 循环执行

grepeat() iterates over a sequence and executes commands dynamically for each value.  
Supports `gstop` and `gskip` commands for flow control within conditional logic.

grepeat() 遍历序列，并动态执行每个值的命令，支持`gstop`和`gskip`用于控制循环流。

Arguments | 参数:
- what (str): Name of the loop variable | 循环变量的名称。
- in_what (list): Sequence to iterate over | 要遍历的序列。
- *do: Commands to execute in each iteration | 每次循环执行的命令。
- share (list): Shared variables in the format [('name', value), ...] | 共享的变量，格式为`[('名称', 值), ...]`

Example | 示例:
grepeat("x", [1, 2, 3], "gout(x)", share=[("number", 5)])
'''

    
    if share!=[]:
        for name in share:
            exec(f"{name[0]}={name[1]}",globals())
    for val in in_what:
        globals()[what] = val
        for command in do:
            dd=command
            try:
                command="xaklsdjizxclvkawengoasjaifnkzncpiaHWEfsjvzos_123456ydcdr="+command
                exec(command,globals())
            except:
                command=dd
                exec(command,globals())
            if xaklsdjizxclvkawengoasjaifnkzncpiaHWEfsjvzos_123456ydcdr == "gstop":
                break
            elif xaklsdjizxclvkawengoasjaifnkzncpiaHWEfsjvzos_123456ydcdr == "gskip":
                continue
        if xaklsdjizxclvkawengoasjaifnkzncpiaHWEfsjvzos_123456ydcdr == "gstop":
            break
        elif xaklsdjizxclvkawengoasjaifnkzncpiaHWEfsjvzos_123456ydcdr == "gskip":
            continue


### Function 7: gloop() ###
def gloop(till_when, *do,share=[]):
    '''
While Loop Execution | 循环执行

gloop() executes commands repeatedly while a condition evaluates to `True`.  
Supports `gstop` and `gskip` commands for flow control within conditional logic.

gloop() 当条件为True时重复执行命令，支持`gstop`和`gskip`用于控制循环流。

Arguments | 参数:
- till_when (str): The condition to evaluate | 循环条件。
- *do: Commands to execute in each iteration | 每次循环执行的命令。
- share (list): Shared variables in the format [('name', value), ...] | 共享的变量，格式为`[('名称', 值), ...]`

Example | 示例:
x = 0
gloop("x < 5", "gout(x)", "x += 1", share=[("multiplier", 2)])
'''

    if share!=[]:
        for name in share:
            exec(f"{name[0]}={name[1]}",globals())
    while eval(till_when, globals()):
        for command in do:
            dd=command
            try:
                command="xaklsdjizxclvkawengoasjaifnkzncpiaHWEfsjvzos_123456ydcdr="+command
                exec(command,globals())
            except:
                command=dd
                exec(command,globals())
            if xaklsdjizxclvkawengoasjaifnkzncpiaHWEfsjvzos_123456ydcdr == "gstop":
                break
            elif xaklsdjizxclvkawengoasjaifnkzncpiaHWEfsjvzos_123456ydcdr == "gskip":
                continue
        if xaklsdjizxclvkawengoasjaifnkzncpiaHWEfsjvzos_123456ydcdr == "gstop":
            break
        elif xaklsdjizxclvkawengoasjaifnkzncpiaHWEfsjvzos_123456ydcdr == "gskip":
            continue
### Function 8: gran_int()###           
def gran_int(start,done):
    '''
Generate Random Integer | 生成随机整数

gran_int() generates a random integer between a given start and end (inclusive).
gran_int() 生成一个给定范围内的随机整数（包含起始和结束值）。

Arguments | 参数:
- start (int): The starting value of the range | 范围的起始值。
- done (int): The ending value of the range | 范围的结束值。

Returns | 返回:
- int: Random integer between start and done | 起始值和结束值之间的随机整数。

Example | 示例:
random_number = gran_int(1, 10)
gout(f"A random number between 1 and 10: {random_number}")
'''

    return random.randint(start,done+1)
### Function 9: gran_choice() ###
def gran_choice(what):
    '''
Random Choice | 随机选择

gran_choice() randomly selects an item from a sequence.
gran_choice() 从一个序列中随机选择一个项。

Arguments | 参数:
- what (list): The sequence to choose from | 要选择的序列。

Returns | 返回:
- Any: A randomly selected item from the sequence | 序列中随机选择的一项。

Example | 示例:
options = ["Apple", "Banana", "Cherry"]
selected = gran_choice(options)
gout(f"The random choice is: {selected}")
'''

    return random.choice(what)


### Function 10: gset() ###
def gset(*do):
    '''
Custom Function Creation | 自定义函数创建

gset() dynamically creates reusable functions, and grun() executes them.
gset() 动态创建可复用的函数，grun() 用于执行它们。

Arguments | 参数:
- *do: Commands to include in the custom function | 要包含在函数中的命令。

Example | 示例:
custom_func = gset('gout("Hello from Gentoricass!")', 'gout("Let’s code!")')
grun(custom_func)  # Execute custom function
'''

    func_code = f"""
def func():
    for command in {do}:
        exec(command, globals())
func()"""
    return func_code

### Function 10: grun() ###
def grun(name):
    '''
Custom Function Creation | 自定义函数创建

gset() dynamically creates reusable functions, and grun() executes them.
gset() 动态创建可复用的函数，grun() 用于执行它们。

Arguments | 参数:
- *do: Commands to include in the custom function | 要包含在函数中的命令。

Example | 示例:
custom_func = gset('gout("Hello from Gentoricass!")', 'gout("Let’s code!")')
grun(custom_func)  # Execute custom function
'''

    exec(f"{name}", globals())  # Execute the given function or code globally | 全局执行给定的函数或代码
def __dir__():
    return [
        "gin", "gout", "gif_in", "gwait", "gif_true_false",
        "grepeat", "gloop", "gget", "grun","gran_int","gran_choice"
    ]


# Main program execution starts here
if __name__ == "__main__":  
    x = gin("what is your name?(nextline)")  # Prompt the user for their name, allowing multi-line input
    gout("hi", x, "what's up?(nextline)You good?")  # Greet the user and ask how they are, allowing multi-line output
    y = gif_in("dickily", x)  # Check if the substring "dickily" is in the user's input and store the result in 'y'
    gwait(1)  # Wait for 1 second
    gout(y)  # Output the result of the substring check ("True" or "False")
    gwait(1)  # Wait for another 1 second
    gif_true_false(y, 'gout("sigma")', 'gout("f1")')  # Execute 'gout("sigma")' if 'y' is True, else execute 'gout("f1")'
    test=gset('gout("hi",x,next="no")','gout("hahahaha")')  # Dynamically define a function called 'test'
    grun(test)  # Call 'test' and execute the commands passed to it
    grepeat("x",[0,1,2,3,4,5],"gout(x)")
    x=0
    gloop("x<=10","gout('now is',x)","x+=1")
    gget("math")
    gout(pi)
