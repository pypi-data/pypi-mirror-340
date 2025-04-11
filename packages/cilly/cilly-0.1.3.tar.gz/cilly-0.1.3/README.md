# Cilly 编程语言解释器

Cilly 是一个简单的编程语言解释器，支持基本的语法分析和代码执行。

## 安装

```bash
pip install cilly
```

## REPL 控制台

Cilly 提供了一个交互式的 REPL 控制台，方便您测试和运行代码。

启动 REPL:
```bash
python -m cilly.repl
```

基本命令:
- 输入代码直接执行
- 使用 `Ctrl+D` 或输入 `exit()` 退出

示例:
```cilly
>>> var x = 10
>>> print(x)
10
>>>
```

## 使用示例

```python
from cilly import cilly_lexer, cilly_parser, cilly_eval

# 示例代码
code = """
let x = 10;
let y = 20;
print(x + y);
"""

# 词法分析
tokens = cilly_lexer(code)

# 语法分析
ast = cilly_parser(tokens)

# 执行代码
cilly_eval(ast)
```

## REPL 控制台

Cilly 提供了一个交互式的 REPL 控制台，方便您测试和运行代码。

启动 REPL:
```bash
python -m cilly.repl
```

基本命令:
- 输入代码直接执行
- 使用 `Ctrl+D` 或输入 `exit()` 退出

示例:
```cilly
>>> let x = 10
>>> print(x)
10
>>>
```

## 贡献指南

欢迎贡献代码！请遵循以下步骤：
1. Fork 本项目
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 使用示例

```python
from cilly import cilly_lexer, cilly_parser, cilly_eval

# 示例代码
code = '''
var a = [1, 2, 3];

var child = {
    name: "Alice",
    age: 12,
    height: 145,
    sing: fun(song) { print("sing: ", song); },
    toString: fun() { return "name:" +  name +  " age:" + age + " height:" + height; }
};

print(a[1], child.name);
child.sing("hello world");
print(child.toString());
'''

# 运行代码
tokens = cilly_lexer(code)
ast = cilly_parser(tokens)
cilly_eval(ast, ({}, None))
```

## REPL 控制台

Cilly 提供了一个交互式的 REPL 控制台，方便您测试和运行代码。

启动 REPL:
```bash
python -m cilly.repl
```

基本命令:
- 输入代码直接执行
- 使用 `Ctrl+D` 或输入 `exit()` 退出

示例:
```cilly
>>> let x = 10
>>> print(x)
10
>>>
```

## 许可证

MIT License