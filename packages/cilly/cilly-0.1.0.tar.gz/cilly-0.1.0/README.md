# Cilly 编程语言解释器

Cilly是一个简单的编程语言解释器，支持基本的语法结构、函数定义、数组和结构体操作。

## 特性

- 支持基本的数据类型和运算
- 支持函数定义和调用
- 支持数组和结构体
- 支持条件语句和循环
- 内置简单的打印功能

## 安装

```bash
pip install cilly
```

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

## 许可证

MIT License