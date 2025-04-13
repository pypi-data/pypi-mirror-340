'''
Gentoricass Programming Language | Gentoricass编程语言  
   Built by: Dickily  
   Version: 1.6  

Gentoricass is an intuitive and beginner-friendly programming language that simplifies coding while maintaining Python’s powerful core functionality.  
Gentoricass是一种直观且适合初学者使用的编程语言，它简化了编程任务，同时保留了Python强大的核心功能。  

---

## Features | 特点:
1. **Interactive Input | 交互式输入** (`gin`)  
   Collect user input interactively and process it seamlessly.

2. **Flexible Output | 灵活的输出** (`gout`)  
   Display text and variables with multi-line output and formatting options.

3. **Logical Conditions | 条件控制** (`gif_true_false`, `gif_in`)  
   Execute commands dynamically based on conditions or substring checks.

4. **Loops with Shared Variables | 支持共享变量的循环** (`grepeat`, `gloop`)  
   Simplify repetitive tasks with advanced support for shared variables.

5. **Break & Skip in Loops | 循环中的Break和Skip** (`gstop`, `gskip`)  
   Control loop execution dynamically using `gstop` and `gskip`.

6. **Random Utilities | 随机数支持** (`gran_int`, `gran_choice`)  
   Generate random integers or select random items from sequences.

7. **Fake Data Generation | 虚拟数据生成**  
   Generate realistic fake data for testing and mock applications:  
   - **Fake Name (`gfake_name`)**: Generate names in English or Chinese.  
   - **Fake Address (`gfake_address`)**: Generate addresses in English or Chinese.  
   - **Fake Phone Number (`gfake_phone_number`)**: Generate phone numbers in English or Chinese format.  
   - **Fake Email (`gfake_email`)**: Generate email addresses in English or Chinese format.  

8. **Custom Function Creation | 自定义函数创建** (`gset`, `grun`)  
   Define and execute reusable custom functions effortlessly.

9. **Built-In Documentation | 内置文档支持** (`help(gentoricass)`)  
   Access comprehensive function explanations directly from the programming language.

---

## Usage | 用法:
Call `help(gentoricass)` to view a detailed list of commands and their descriptions.  
调用`help(gentoricass)`可以查看详细的命令列表及其说明。  

---

## Version 1.6 Highlights | 版本1.6亮点:
1. **Enhanced Fake Data Generation**:  
   Expanded functionality to create more realistic names, addresses, phone numbers, and email addresses with support for Chinese and English locales.  

2. **Optimized Loop Management**:  
   Improved handling of `grepeat` and `gloop` loops with enhanced dynamic flow control using shared variables and precise command execution.  

3. **Simplified Function Documentation**:  
   Refined built-in `help()` to provide clearer explanations for all functions.  

4. **Improved Random Utilities**:  
   Further optimization of random number generation (`gran_int`) and random item selection (`gran_choice`) for better usability.  

---

Explore Gentoricass, unlock its powerful yet beginner-friendly features, and start coding smarter today! 🚀  
 
'''



import time  # Import the time module for delays | 导入time模块用于延时
import math# Import the math module for mathematical functions | 导入math模块用于数学功能
from math import *# Import all math attributes | 导入math模块的所有属性
import asyncio  # Import asyncio for asynchronous tasks | 导入asyncio模块用于异步任务
import random
from faker import Faker
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
def gfake_name(chinese=False):
    '''
Generate Fake Name | 生成虚拟姓名

gfake_name() generates a random fake name, either in English or Chinese, based on the specified locale.
gfake_name() 生成随机虚拟姓名，可根据指定语言环境生成英文或中文姓名。

Arguments | 参数:
- chinese (bool, optional): If True, generates a Chinese name. Defaults to False (English name).
  如果为 True，则生成中文姓名。默认值为 False（英文姓名）。

Returns | 返回:
- str: Fake name | 虚拟姓名。

Example | 示例:
# Generate English name
name = gfake_name()
gout("Generated Name:", name)

# Generate Chinese name
chinese_name = gfake_name(chinese=True)
gout("生成的姓名:", chinese_name)
'''

    if chinese:
        fake=Faker(locale="zh_CN")
    else:
        fake=Faker()
    return fake.name()
def gfake_address(chinese=False):
    '''
Generate Fake Address | 生成虚拟地址

gfake_address() generates a random fake address, either in English or Chinese, based on the specified locale.
gfake_address() 生成随机虚拟地址，可根据指定语言环境生成英文或中文地址。

Arguments | 参数:
- chinese (bool, optional): If True, generates a Chinese address. Defaults to False (English address).
  如果为 True，则生成中文地址。默认值为 False（英文地址）。

Returns | 返回:
- str: Fake address | 虚拟地址。

Example | 示例:
# Generate English address
address = gfake_address()
gout("Generated Address:", address)

# Generate Chinese address
chinese_address = gfake_address(chinese=True)
gout("生成的地址:", chinese_address)
'''

    if chinese:
        fake=Faker(locale="zh_CN")
    else:
        fake=Faker()
    return fake.address()
def gfake_phone_number(chinese=False):
    '''
Generate Fake Phone Number | 生成虚拟电话号码

gfake_phone_number() generates a random fake phone number, either in English or Chinese format, based on the specified locale.
gfake_phone_number() 生成随机虚拟电话号码，可根据指定语言环境生成英文或中文格式。

Arguments | 参数:
- chinese (bool, optional): If True, generates a Chinese phone number. Defaults to False (English format).
  如果为 True，则生成中文电话号码。默认值为 False（英文格式）。

Returns | 返回:
- str: Fake phone number | 虚拟电话号码。

Example | 示例:
# Generate English phone number
phone_number = gfake_phone_number()
gout("Generated Phone Number:", phone_number)

# Generate Chinese phone number
chinese_phone_number = gfake_phone_number(chinese=True)
gout("生成的电话号码:", chinese_phone_number)
'''

    if chinese:
        fake=Faker(locale="zh_CN")
    else:
        fake=Faker()
    return fake.phone_number()
def gfake_email(chinese=False):
    '''
Generate Fake Email | 生成虚拟邮箱地址

gfake_email() generates a random fake email address, either in English or Chinese format, based on the specified locale.
gfake_email() 生成随机虚拟邮箱地址，可根据指定语言环境生成英文或中文格式。

Arguments | 参数:
- chinese (bool, optional): If True, generates a Chinese-style email address. Defaults to False (English format).
  如果为 True，则生成中文邮箱地址。默认值为 False（英文格式）。

Returns | 返回:
- str: Fake email address | 虚拟邮箱地址。

Example | 示例:
# Generate English email address
email = gfake_email()
gout("Generated Email:", email)

# Generate Chinese email address
chinese_email = gfake_email(chinese=True)
gout("生成的邮箱地址:", chinese_email)
'''

    if chinese:
        fake=Faker(locale="zh_CN")
    else:
        fake=Faker()
    return fake.email()
def __dir__():
    return [
        "gin", "gout", "gif_in", "gwait", "gif_true_false",
        "grepeat", "gloop", "gget", "grun","gran_int","gran_choice",
        "gfake_name","gfake_address","gfake_phone_number","gfake_email"
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
    gout(gfake_name())
    gout(gfake_address())
    gout(gfake_phone_number())
    gout(gfake_email())
    gout(gfake_name(chinese=True))
    gout(gfake_address(chinese=True))
    gout(gfake_phone_number(chinese=True))
    gout(gfake_email(chinese=True))