def cilly_analyzer(ast):
    """分析AST并返回分析结果
    Args:
        ast: 解析后的AST
    Returns:
        dict: 包含分析结果的字典
    """
    analysis = {
        'variables': set(),  # 变量定义
        'functions': set(),  # 函数定义
        'function_calls': set(),  # 函数调用
        'loops': 0,  # 循环数量
        'conditionals': 0,  # 条件语句数量
        'array_ops': 0,  # 数组操作数量
        'struct_ops': 0,  # 结构体操作数量
    }

    def analyze_node(node):
        if not isinstance(node, list):
            return

        node_type = node[0] if node else None

        if node_type == 'define':
            analysis['variables'].add(node[1])
            analyze_node(node[2])

        elif node_type == 'fun':
            if len(node) > 2:
                analysis['functions'].add(tuple(node[1]))  # 将参数列表转换为元组以便存储
                analyze_node(node[2])

        elif node_type == 'call':
            if isinstance(node[1], list) and node[1][0] == 'id':
                analysis['function_calls'].add(node[1][1])
            for arg in node[2]:
                analyze_node(arg)

        elif node_type == 'while':
            analysis['loops'] += 1
            analyze_node(node[1])
            analyze_node(node[2])

        elif node_type == 'if':
            analysis['conditionals'] += 1
            analyze_node(node[1])
            analyze_node(node[2])
            if node[3]:  # else 分支
                analyze_node(node[3])

        elif node_type == 'array':
            analysis['array_ops'] += 1
            for item in node[1]:
                analyze_node(item)

        elif node_type == 'struct':
            analysis['struct_ops'] += 1
            for value in node[1].values():
                analyze_node(value)

        elif node_type == 'program':
            for statement in node[1]:
                analyze_node(statement)

        elif isinstance(node, list):
            for item in node[1:] if len(node) > 1 else []:
                analyze_node(item)

    analyze_node(ast)

    # 转换集合为列表以便更好地显示
    analysis['variables'] = list(analysis['variables'])
    analysis['functions'] = [list(f) for f in analysis['functions']]
    analysis['function_calls'] = list(analysis['function_calls'])

    return analysis