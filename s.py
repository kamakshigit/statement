import ast

def visit_Assign(self, node):
    target = node.targets[0].id
    value = self.visit(node.value)

    if isinstance(node.value, ast.Constant):
        if isinstance(node.value.value, int):
            type_ = 'int'
        elif isinstance(node.value.value, float):
            type_ = 'float'
        elif isinstance(node.value.value, str):
            type_ = 'string'
    else:
        type_ = 'auto'

    if target not in self.variables:
        self.variables[target] = type_
        self.write_line(f'{type_} {target} = {value};')
    else:
        self.write_line(f'{target} = {value};')

def visit_Expr(self, node):
    if isinstance(node.value, ast.Call) and getattr(node.value.func, 'id', '') == 'print':
        args = ' << " " << '.join([self.visit(arg) for arg in node.value.args])
        self.write_line(f'cout << {args} << endl;')
    else:
        self.write_line(self.visit(node.value) + ';')

def visit_If(self, node):
    current = node
    first = True

    while True:
        test = self.visit(current.test)
        if first:
            self.write_line(f'if ({test}) {{')
            first = False
        else:
            self.write_line(f'else if ({test}) {{')

        self.indent += 1
        for stmt in current.body:
            self.visit(stmt)
        self.indent -= 1
        self.write_line('}')

        # If there's exactly one statement in orelse and it's an If node -> it's an elif
        if len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
            current = current.orelse[0]
        else:
            break

    # Handle final else block, if any
    if current.orelse:
        self.write_line('else {')
        self.indent += 1
        for stmt in current.orelse:
            self.visit(stmt)
        self.indent -= 1
        self.write_line('}')

def visit_While(self, node):
    test = self.visit(node.test)
    self.write_line(f'while ({test}) {{')
    self.indent += 1
    for stmt in node.body:
        self.visit(stmt)
    self.indent -= 1
    self.write_line('}')

def visit_For(self, node):
    if isinstance(node.iter, ast.Call) and node.iter.func.id == 'range':
        args = [self.visit(arg) for arg in node.iter.args]
        var = node.target.id
        if len(args) == 1:
            start, end = '0', args[0]
        else:
            start, end = args
        self.write_line(f'for (int {var} = {start}; {var} < {end}; {var}++) {{')
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1
        self.write_line('}')

        def visit_Pass(self, node):
            self.write_line('// pass')

        def visit_Break(self, node):
            self.write_line('break;')

        def visit_Continue(self, node):
            self.write_line('continue;')
