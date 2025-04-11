import sys
import os
from cilly.compiler import cilly_lexer, cilly_parser, cilly_eval

# Windows平台使用pyreadline3替代readline
try:
    import readline
except ImportError:
    try:
        import pyreadline3 as readline
    except ImportError:
        # 如果pyreadline3也不可用，则跳过readline功能
        pass

class CillyREPL:
    def __init__(self):
        self.env = ({}, None)  # 初始化环境
        self.history = []      # 命令历史记录
        self.multiline_code = []
        self.is_multiline = False

    def get_input_prompt(self):
        return '... ' if self.is_multiline else 'cilly> '

    def handle_input(self, line):
        stripped_line = line.strip()
        
        # 处理空行
        if stripped_line == '':
            if self.is_multiline:
                # 空行结束多行输入
                code = '\n'.join(self.multiline_code)
                self.multiline_code = []
                self.is_multiline = False
                return code
            return None

        # 检查是否需要进入多行模式
        if not self.is_multiline:
            # 检查未闭合的括号或以特定字符结尾
            open_count = stripped_line.count('{')
            close_count = stripped_line.count('}')
            if open_count > close_count or stripped_line.endswith('{'):
                self.is_multiline = True

        # 处理多行模式
        if self.is_multiline:
            self.multiline_code.append(line)
            # 检查是否可以结束多行模式
            current_code = '\n'.join(self.multiline_code)
            open_count = current_code.count('{')
            close_count = current_code.count('}')
            if open_count == close_count and not stripped_line.endswith('\\'):
                # 括号已平衡，可以尝试结束多行模式
                if not any(current_code.strip().endswith(x) for x in ['{', '\\', ',']):
                    code = current_code
                    self.multiline_code = []
                    self.is_multiline = False
                    return code
            return None

        return line

    def evaluate(self, code):
        if not code:
            return

        try:
            tokens = cilly_lexer(code)
            ast = cilly_parser(tokens)
            result = cilly_eval(ast, self.env)
            if result is not None:
                print('结果:', result)
        except Exception as e:
            print('错误:', str(e))

    def run(self):
        print('欢迎使用Cilly REPL!')
        print('输入代码开始执行，空行结束多行输入，Ctrl+C退出\n')

        while True:
            try:
                line = input(self.get_input_prompt())
                code = self.handle_input(line)
                
                if code is not None:
                    self.history.append(code)
                    self.evaluate(code)

            except KeyboardInterrupt:
                print('\n再见！')
                break
            except EOFError:
                break

def main():
    repl = CillyREPL()
    repl.run()

if __name__ == '__main__':
    main()