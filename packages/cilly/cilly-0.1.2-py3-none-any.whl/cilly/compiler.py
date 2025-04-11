import turtle


def error(src, msg):
    raise Exception(f'{src} : {msg}')


def mk_tk(tag, val=None):
    return [tag, val]


def tk_tag(t):
    return t[0]


def tk_val(t):
    return t[1]


def make_str_reader(s, err):
    cur = None
    pos = -1

    def peek(p=0):
        if pos + p >= len(s):
            return 'eof'
        else:
            return s[pos + p]

    def match(c):
        if c != peek():
            err(f'期望{c}, 实际{peek()}')

        return next()

    def next():
        nonlocal pos, cur

        old = cur
        pos = pos + 1
        if pos >= len(s):
            cur = 'eof'
        else:
            cur = s[pos]

        return old

    next()
    return peek, match, next


# 添加了 ':' 到 cilly_op1 列表
cilly_op1 = [
    '(', ')', '{', '}', ',', ';',
    '+', '-', '*', '/', '%', '[', ']', '.', ':'
]

cilly_op2 = {
    '>': '>=',
    '<': '<=',
    '=': '==',
    '!': '!=',
    '&': '&&',
    '|': '||',
}

cilly_keywords = [
    'var', 'print', 'if', 'else', 'while', 'break', 'continue', 'return', 'fun',
    'true', 'false', 'null',
]


def cilly_lexer(prog):
    def err(msg):
        error('cilly lexer', msg)

    peek, match, next = make_str_reader(prog, err)

    def program():
        r = []

        while True:
            skip_ws()
            if peek() == 'eof':
                break

            r.append(token())

        return r

    def skip_ws():
        while peek() in [' ', '\t', '\r', '\n']:
            next()

    def token():

        c = peek()

        if is_digit(c):
            return num()

        if c == '"':
            return string()

        if c == '_' or is_alpha(c):
            return id()

        if c in cilly_op1:
            next()
            return mk_tk(c)

        if c in cilly_op2:
            next()
            if peek() == cilly_op2[c][1]:
                next()
                return mk_tk(cilly_op2[c])
            else:
                return mk_tk(c)

        err(f'非法字符{c}')

    def is_digit(c):
        return c >= '0' and c <= '9'

    def num():
        r = ''

        while is_digit(peek()):
            r = r + next()

        if peek() == '.':
            r = r + next()

            while is_digit(peek()):
                r = r + next()

        return mk_tk('num', float(r) if '.' in r else int(r))

    def string():
        match('"')

        r = ''
        while peek() != '"' and peek() != 'eof':
            r = r + next()

        match('"')

        return mk_tk('str', r)

    def is_alpha(c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')

    def is_digit_alpha__(c):
        return c == '_' or is_digit(c) or is_alpha(c)

    def id():
        r = '' + next()

        while is_digit_alpha__(peek()):
            r = r + next()

        if r in cilly_keywords:
            return mk_tk(r)

        return mk_tk('id', r)

    return program()


EOF = mk_tk('eof')


def make_token_reader(ts, err):
    pos = -1
    cur = None

    def peek(p=0):
        if pos + p >= len(ts):
            return 'eof'
        else:
            return tk_tag(ts[pos + p])

    def match(t):
        if peek() != t:
            err(f'期望{t},实际为{cur}')

        return next()

    def next():
        nonlocal pos, cur

        old = cur
        pos = pos + 1

        if pos >= len(ts):
            cur = EOF
        else:
            cur = ts[pos]

        return old

    next()

    return peek, match, next


def cilly_parser(tokens):
    def err(msg):
        error('cilly parser', msg)

    peek, match, next = make_token_reader(tokens, err)

    def program():

        r = []

        while peek() != 'eof':
            r.append(statement())

        return ['program', r]

    def statement():
        t = peek()

        if t == 'var':
            return define_stat()

        if t == 'id' and peek(1) == '=':
            return assign_stat()

        if t == 'print':
            return print_stat()

        if t == 'if':
            return if_stat()

        if t == 'while':
            return while_stat()

        if t == 'break':
            return break_stat()

        if t == 'continue':
            return continue_stat()

        if t == 'return':
            return return_stat()

        if t == '{':
            return block_stat()

        return expr_stat()

    def define_stat():
        match('var')

        id = tk_val(match('id'))

        match('=')

        e = expr()

        match(';')

        return ['define', id, e]

    def assign_stat():
        id = tk_val(match('id'))

        match('=')

        e = expr()

        match(';')

        return ['assign', id, e]

    def print_stat():
        match('print')
        match('(')

        if peek() == ')':
            alist = []
        else:
            alist = args()

        match(')')
        match(';')

        return ['print', alist]

    def args():

        r = [expr()]

        while peek() == ',':
            match(',')
            r.append(expr())

        return r

    def if_stat():  # if ( expr ) statement (else statment)?
        match('if')
        match('(')
        cond = expr()
        match(')')

        true_stat = statement()

        if peek() == 'else':
            match('else')
            false_stat = statement()
        else:
            false_stat = None
        return ['if', cond, true_stat, false_stat]

    def while_stat():
        match('while')
        match('(')
        cond = expr()
        match(')')
        body = statement()

        return ['while', cond, body]

    def continue_stat():
        match('continue')
        match(';')

        return ['continue']

    def break_stat():
        match('break')
        match(';')
        return ['break']

    def return_stat():
        match('return')

        if peek() != ';':
            e = expr()
        else:
            e = None

        match(';')

        return ['return', e]

    def block_stat():
        match('{')

        r = []

        while peek() != '}':
            r.append(statement())

        match('}')
        return ['block', r]

    def expr_stat():
        e = expr()
        match(';')

        return ['expr_stat', e]

    def literal(bp=0):
        return next()

    def unary(bp):
        op = tk_tag(next())
        e = expr(bp)

        return ['unary', op, e]

    def fun_expr(bp=0):
        match('fun')
        match('(')
        if peek() == ')':
            plist = []
        else:
            plist = params()

        match(')')
        body = block_stat()

        return ['fun', plist, body]

    def params():
        r = [tk_val(match('id'))]

        while peek() == ',':
            match(',')
            r.append(tk_val(match('id')))

        return r

    def parens(bp=0):
        match('(')

        e = expr()

        match(')')

        return e

    def array_expr(bp=0):
        match('[')
        if peek() == ']':
            arr = []
        else:
            arr = args()
        match(']')
        return ['array', arr]

    def struct_expr(bp=0):
        match('{')
        fields = {}
        while peek() != '}':
            field_name = tk_val(match('id'))
            match(':')
            field_value = expr()
            fields[field_name] = field_value
            if peek() == ',':
                match(',')
        match('}')
        return ['struct', fields]

    def access_expr(left, bp=0):
        match('.')
        field = tk_val(match('id'))
        return ['access', left, field]

    def index_expr(left, bp=0):
        match('[')
        index = expr()
        match(']')
        return ['index', left, index]

    op1 = {
        'id': (100, literal),
        'num': (100, literal),
        'str': (100, literal),
        'true': (100, literal),
        'false': (100, literal),
        'null': (100, literal),
        '-': (85, unary),
        '!': (85, unary),
        'fun': (98, fun_expr),
        '(': (100, parens),
        '[': (95, array_expr),
        '{': (95, struct_expr)
    }

    def get_op1_parser(t):
        if t not in op1:
            err(f'非法token: {t}')

        return op1[t]

    def binary(left, bp):

        op = tk_tag(next())

        right = expr(bp)

        return ['binary', op, left, right]

    def call(fun_expr, bp=0):
        match('(')
        if peek() != ')':
            alist = args()
        else:
            alist = []
        match(')')
        return ['call', fun_expr, alist]

    op2 = {
        '*': (80, 81, binary),
        '/': (80, 81, binary),
        '%': (80, 81, binary),
        '+': (70, 71, binary),
        '-': (70, 71, binary),
        '>': (60, 61, binary),
        '>=': (60, 61, binary),
        '<': (60, 61, binary),
        '<=': (60, 61, binary),
        '==': (50, 51, binary),
        '!=': (50, 51, binary),
        '&&': (40, 41, binary),
        '||': (30, 31, binary),
        '(': (90, 91, call),
        '.': (92, 93, access_expr),
        '[': (92, 93, index_expr)
    }

    def get_op2_parser(t):
        if t not in op2:
            return (0, 0, None)
        else:
            return op2[t]

    def expr(bp=0):
        r_bp, parser = get_op1_parser(peek())
        left = parser(r_bp)

        while True:
            l_bp, r_bp, parser = get_op2_parser(peek())
            if parser is None or l_bp <= bp:
                break

            left = parser(left, r_bp)

        return left

    return program()


def mk_num(i):
    return ['num', i]


def mk_str(s):
    return ['str', s]


def mk_proc(params, body, env):
    return ['proc', params, body, env]


def mk_primitive_proc(f):
    return ['primitive', f]


TRUE = ['bool', True]
FALSE = ['bool', False]


def mk_bool(b):
    return TRUE if b else FALSE


NULL = ['null', None]


def val(v):
    return v[1]


# 环境: ({x:1, y:2},parent_env)
def lookup_var(env, name):
    while env:
        e, env = env

        if name in e:
            return e[name]

    error('lookup var', f'变量未定义{name}')


def set_var(env, name, val):
    while env:
        e, env = env
        if name in e:
            e[name] = val
            return

    error('set var', f'变量未定义{name}')


def define_var(env, name, val):
    e, env = env

    if name in e:
        error('define var', f'变量已定义{name}')

    e[name] = val


def extend_env(vars, vals, env):
    e = {var: val for (var, val) in zip(vars, vals)}
    return (e, env)


# 定义 cilly_greet 函数
def cilly_greet(name):
    print(f"Hello, {val(name)}!")
    return NULL


env = ({
    'cilly_greet': mk_primitive_proc(cilly_greet)
}, None)


def cilly_eval(ast, env):
    def err(msg):
        return error('cilly eval', msg)

    def ev_program(node, env):
        _, statements = node

        r = NULL

        for s in statements:
            r = visit(s, env)
            if tk_tag(r) == 'return':
                return r

        # 只在有明确返回值时才返回结果
        if r != NULL and r != ['return', NULL]:
            return r

    def ev_expr_stat(node, env):
        _, e = node

        return visit(e, env)

    def ev_print(node, env):
        _, args = node

        for a in args:
            print(val(visit(a, env)), end=' ')

        print('')

        return NULL

    def ev_literal(node, env):
        tag, val = node

        if tag in ['num', 'str']:
            return node

        if tag in ['true', 'false']:
            return TRUE if tag == 'true' else FALSE

        if tag == 'null':
            return NULL

        err(f'非法字面量{node}')

    def ev_unary(node, env):
        _, op, e = node

        v = val(visit(e, env))

        if op == '-':
            return mk_num(-v)

        if op == '!':
            return mk_bool(not (v))

        err(f'非法一元运算符{op}')

    def ev_binary(node, env):
        _, op, e1, e2 = node

        v1 = val(visit(e1, env))

        if op == '&&':
            if v1 == False:
                return FALSE
            else:
                return visit(e2, env)

        if op == '||':
            if v1 == True:
                return TRUE
            else:
                return visit(e2, env)

        v2 = val(visit(e2, env))

        if isinstance(v1, str) and isinstance(v2, int):
            v2 = str(v2)

        if isinstance(v1, int) and isinstance(v2, str):
            v1 = str(v1)

        if op == '+':
            return mk_str(str(v1) + str(v2)) if isinstance(v1, str) or isinstance(v2, str) else mk_num(v1 + v2)

        if op == '-':
            return mk_num(v1 - v2)

        if op == '*':
            return mk_num(v1 * v2)

        if op == '/':
            return mk_num(v1 / v2)

        if op == '%':
            return mk_num(v1 % v2)

        if op == '>':
            return mk_bool(v1 > v2)

        if op == '>=':
            return mk_bool(v1 >= v2)

        if op == '<':
            return mk_bool(v1 < v2)

        if op == '<=':
            return mk_bool(v1 <= v2)

        if op == '==':
            return mk_bool(v1 == v2)

        if op == '!=':
            return mk_bool(v1 != v2)

        err(f'非法二元运算符{op}')

    def ev_if(node, env):
        _, cond, true_stat, false_stat = node
        cond_val = val(visit(cond, env))
        if cond_val:
            return visit(true_stat, env)
        elif false_stat:
            return visit(false_stat, env)
        return NULL

    def ev_while(node, env):
        _, cond, body = node
        while True:
            cond_val = val(visit(cond, env))
            if not cond_val:
                break
            r = visit(body, env)
            if tk_tag(r) == 'break':
                break
            if tk_tag(r) == 'continue':
                continue
            if tk_tag(r) == 'return':
                return r
        return NULL

    def ev_break(node, env):
        return ['break']

    def ev_continue(node, env):
        return ['continue']

    def ev_return(node, env):
        _, e = node
        if e is None:
            return ['return', NULL]
        return ['return', visit(e, env)]

    def ev_block(node, env):
        _, statements = node
        r = NULL
        new_env = extend_env([], [], env)
        for s in statements:
            r = visit(s, new_env)
            if tk_tag(r) in ['break', 'continue', 'return']:
                return r
        return r

    def ev_define(node, env):
        _, id, e = node
        define_var(env, id, visit(e, env))
        return NULL

    def ev_assign(node, env):
        _, id, e = node
        set_var(env, id, visit(e, env))
        return NULL

    def ev_call(node, env):
        _, fun_expr, args = node
        fun_val = visit(fun_expr, env)
        # 检查 fun_val 是否为返回值
        if tk_tag(fun_val) == 'return':
            fun_val = fun_val[1]
        if tk_tag(fun_val) == 'primitive':
            arg_vals = [visit(arg, env) for arg in args]
            return fun_val[1](*arg_vals)
        elif tk_tag(fun_val) == 'proc':
            params, body, fun_env = fun_val[1:]
            arg_vals = [visit(arg, env) for arg in args]
            # 检查是否是结构体方法调用
            if tk_tag(fun_expr) == 'access':
                struct_obj = visit(fun_expr[1], env)
                if tk_tag(struct_obj) == 'struct':
                    # 把结构体作为 this 传递给方法
                    new_env = extend_env(['this'] + params, [struct_obj] + arg_vals, fun_env)
                    return visit(body, new_env)
            new_env = extend_env(params, arg_vals, fun_env)
            return visit(body, new_env)
        err(f'不是可调用对象: {fun_val}')

    def ev_access(node, env):
        _, struct_expr, field = node
        struct_obj = visit(struct_expr, env)
        if tk_tag(struct_obj) == 'struct':
            fields = struct_obj[1]
            if field in fields:
                return visit(fields[field], env)
        err(f'非法结构体访问: {struct_expr}')

    def ev_index(node, env):
        _, array_expr, index_expr = node
        array_obj = visit(array_expr, env)
        index_val = val(visit(index_expr, env))
        if tk_tag(array_obj) == 'array':
            arr = array_obj[1]
            if 0 <= index_val < len(arr):
                return visit(arr[index_val], env)
        err(f'非法数组索引: {array_expr}')

    def ev_fun(node, env):
        _, params, body = node
        return mk_proc(params, body, env)

    def ev_id(node, env):
        _, id = node
        # 检查是否为 this 变量
        if id == 'this':
            return lookup_var(env, id)
        # 尝试从当前环境查找变量
        try:
            return lookup_var(env, id)
        except Exception:
            # 尝试从 this 中查找字段
            this_obj = lookup_var(env, 'this')
            if tk_tag(this_obj) == 'struct':
                fields = this_obj[1]
                if id in fields:
                    return fields[id]
        error('lookup var', f'变量未定义{id}')

    def ev_array(node, env):
        _, elements = node
        evaluated_elements = [visit(e, env) for e in elements]
        return ['array', evaluated_elements]

    def ev_struct(node, env):
        _, fields = node
        evaluated_fields = {name: visit(value, env) for name, value in fields.items()}
        return ['struct', evaluated_fields]

    def visit(node, env):
        tag = tk_tag(node)

        if tag == 'program':
            return ev_program(node, env)
        if tag == 'expr_stat':
            return ev_expr_stat(node, env)
        if tag == 'print':
            return ev_print(node, env)
        if tag in ['num', 'str', 'true', 'false', 'null']:
            return ev_literal(node, env)
        if tag == 'unary':
            return ev_unary(node, env)
        if tag == 'binary':
            return ev_binary(node, env)
        if tag == 'if':
            return ev_if(node, env)
        if tag == 'while':
            return ev_while(node, env)
        if tag == 'break':
            return ev_break(node, env)
        if tag == 'continue':
            return ev_continue(node, env)
        if tag == 'return':
            return ev_return(node, env)
        if tag == 'block':
            return ev_block(node, env)
        if tag == 'define':
            return ev_define(node, env)
        if tag == 'assign':
            return ev_assign(node, env)
        if tag == 'call':
            return ev_call(node, env)
        if tag == 'access':
            return ev_access(node, env)
        if tag == 'index':
            return ev_index(node, env)
        if tag == 'fun':
            return ev_fun(node, env)
        if tag == 'id':
            return ev_id(node, env)
        if tag == 'array':
            return ev_array(node, env)
        if tag == 'struct':
            return ev_struct(node, env)
        if tag == 'proc':
            return node
        err(f'非法节点{node}')

    return visit(ast, env)




# 创建turtle环境变量
def mk_turtle_proc(f):
    return mk_primitive_proc(lambda *args: ['null', f(*[val(arg) for arg in args])])

turtle_env = ({
    'turtle_forward': mk_turtle_proc(turtle.forward),
    'turtle_backward': mk_turtle_proc(turtle.backward),
    'turtle_right': mk_turtle_proc(turtle.right),
    'turtle_left': mk_turtle_proc(turtle.left),
    'turtle_penup': mk_turtle_proc(turtle.penup),
    'turtle_pendown': mk_turtle_proc(turtle.pendown),
    'turtle_pencolor': mk_turtle_proc(turtle.pencolor),
}, env)

    