from sys import exit

from math import e, pi

toggle_print_create = True

ids = list()
data = list()
history = list()


class Text:
    def __init__(self, value):
        self.value = value

    def present(self):
        return self.value


class Number:
    def __init__(self, value):
        self.value = value

    def present(self):
        ret = str(self.value)
        if self.is_integer():
            return ret[:-2]
        return ret

    def is_integer(self):
        return str(self.value).endswith('.0')

    @staticmethod
    def add_numbers(n, m):
        return Number(n.value + m.value)

    @staticmethod
    def mul_numbers(n, m):
        return Number(n.value * m.value)

    @staticmethod
    def div_numbers(n, m):
        return Number(n.value / m.value)

    @staticmethod
    def sub_numbers(n, m):
        return Number(n.value - m.value)

    @staticmethod
    def pow_numbers(n, m):
        return Number(n.value ** m.value)

    @staticmethod
    def absolute_value(n):
        return Number(abs(n.value))


class Vector:
    def __init__(self, components):
        self.components = components

    def present(self):
        presentation = '('
        for i in self.components:
            presentation += i.present() + ', '
        return presentation[:-2] + ')'

    def dimension(self):
        return len(self.components)

    @staticmethod
    def add_vectors(v, u):
        if v.dimension() != u.dimension():
            return Error('Vectors must have the same dimension')
        return Vector([Number.add_numbers(v.components[i], u.components[i]) for i in range(v.dimension())])

    @staticmethod
    def sub_vectors(v, u):
        if v.dimension() != u.dimension():
            return Error('Vectors must have the same dimension')
        return Vector([Number.sub_numbers(v.components[i], u.components[i]) for i in range(v.dimension())])

    @staticmethod
    def dot_product(v, u):
        if v.dimension() != u.dimension():
            return Error('Vectors must have the same dimension')
        result = 0
        for i in range(v.dimension()):
            result += v.components[i].value * u.components[i].value
        return Number(result)

    @staticmethod
    def mul_number_vector(n, v):
        return Vector([Number.mul_numbers(v.components[i], n) for i in range(v.dimension())])

    @staticmethod
    def component(v, index):
        if not index.is_integer():
            return Error('Component index must be an integer')
        if index.value > v.dimension():
            return Error('Index must be less than or equal to the vector\' dimension')
        return v.components[int(index.value) - 1]

    @staticmethod
    def norm(v):
        return Number.pow_numbers(Vector.dot_product(v, v), Number(0.5))

    @staticmethod
    def zero_vector(n):
        if not n.is_integer():
            return Error('Dimension of zero vector must be an integer')
        return Vector([Number(0) for i in range(int(n.value))])


class Matrix:
    def __init__(self, entries):
        self.entries = entries

    def present(self):
        longest = 0
        for row in self.entries:
            for entry in row[:-1]:
                if len(entry.present()) > longest:
                    longest = len(entry.present())

        result = str()
        longest += 3  # add buffer
        for row in self.entries:
            for entry in row:
                result += entry.present() + ' ' * (longest - len(entry.present()))
            result = result.rstrip()
            result += '\n'
        return result[:-1]

    def rows(self):
        return len(self.entries)

    def columns(self):
        return len(self.entries[0])

    @staticmethod
    def mul_matrix_vector(m, v):
        if m.columns() != v.dimension():
            return Error('Number of matrix columns must equal number vector rows')
        components = list()
        for i in range(m.rows()):
            components.append(Vector.dot_product(v, Vector(m.entries[i])))
        return Vector(components)

    @staticmethod
    def mul_matrix_matrix(a, b):
        if a.columns() != b.rows():
            return Error('Number of first matrix\'s columns must equal number of second matrix\'s rows')
        entries = list()
        for i in range(a.rows()):
            row = list()
            for j in range(b.columns()):
                row.append(Vector.dot_product(Vector(a.entries[i]), Vector([entry[j] for entry in b.entries])))
            entries.append(row)
        return Matrix(entries)

    @staticmethod
    def add_matrices(a, b):
        if a.rows() != b.rows() or a.columns() != b.columns():
            return Error('Matrices must have the same number of rows and columns')
        entries = list()
        for i in range(a.rows()):
            row = list()
            for j in range(a.columns()):
                row.append(Number.add_numbers(a.entries[i][j], b.entries[i][j]))
            entries.append(row)
        return Matrix(entries)

    @staticmethod
    def sub_matrices(a, b):
        if a.rows() != b.rows() or a.columns() != b.columns():
            return Error('Matrices must have the same number of rows and columns')
        entries = list()
        for i in range(a.rows()):
            row = list()
            for j in range(a.columns()):
                row.append(Number.sub_numbers(a.entries[i][j], b.entries[i][j]))
            entries.append(row)
        return Matrix(entries)

    @staticmethod
    def entry(m, row, col):
        if not (row.is_integer() and col.is_integer()):
            return Error('Row and column indices must be integer')
        if row.value > m.rows() or col.value > m.columns():
            return Error('Row and column indices must be less than or equal to the matrix\'s row and column counts '
                         'respectively')
        return m.entries[int(row.value) - 1][int(col.value) - 1]

    @staticmethod
    def identity_matrix(n):
        if not n.is_integer():
            return Error('Size of identity matrix must be an integer')
        num = int(n.value)
        entries = list()
        for i in range(num):
            row = list()
            for j in range(num):
                if j == i:
                    row.append(Number(1))
                else:
                    row.append(Number(0))
            entries.append(row)
        return Matrix(entries)

    @staticmethod
    def zero_matrix(n):
        if not n.is_integer():
            return Error('Size of zero matrix must be an integer')
        row = [Number(0) for i in range(int(n.value))]
        return Matrix([row for i in range(int(n.value))])

    @staticmethod
    def trace(m):
        if m.columns() != m.rows():
            return Error('Trace is only defined for square matrices')
        sum = 0
        for i in range(m.columns()):
            sum += m.entries[i][i].value
        return Number(sum)

    @staticmethod
    def latex(m, type):
        type_value = type.value

        if type_value != 'n' and type_value != 'p' and type_value != 'b' and type_value != 'v':
            return Error(type_value + ' is not a valid matrix delimiter')

        res = str()
        for row in m.entries:
            for entry in row:
                res += entry.present() + '&'
            res = res[:-1] + '\\\\'
        res = res[:-2]

        if type_value == 'n':
            res = '\\begin{matrix}' + res + '\\end{matrix}'
        elif type_value == 'p':
            res = '\\begin{pmatrix}' + res + '\\end{pmatrix}'
        elif type_value == 'b':
            res = '\\begin{bmatrix}' + res + '\\end{bmatrix}'
        elif type_value == 'v':
            res = '\\begin{vmatrix}' + res + '\\end{vmatrix}'
        return Text(res)


class Error:
    def __init__(self, msg):
        self.msg = msg

    def present(self):
        return self.msg


def find_comma(ln):
    count = 0
    for i in range(len(ln)):
        if ln[i] == ',' and count == 1:
            return i
        elif ln[i] == '(' or ln[i] == '[':
            count += 1
        elif ln[i] == ')' or ln[i] == ']':
            count -= 1


def general_two_function(size, va):
    comma = find_comma(va)
    return translate(va[size + 1: comma].strip()), translate(va[comma + 1: -1].strip())


def general_three_function(size, va):
    comma1 = find_comma(va)
    comma2 = find_comma('(' + va[comma1 + 1:]) + comma1
    m1 = translate(va[size + 1: comma1].strip())
    m2 = translate(va[comma1 + 1: comma2].strip())
    m3 = translate(va[comma2 + 1: -1].strip())
    return m1, m2, m3


def translate(va):
    # Translates an expression into a single object
    try:
        f = float(va)
        return Number(f)
    except ValueError:
        pass

    if va == 'e':
        return Number(e)
    elif va == 'pi':
        return Number(pi)

    elif ids.__contains__(va):
        return data[ids.index(va)]

    elif va.startswith('('):
        return Vector([translate(x.strip()) for x in va[1: -1].split(',')])

    elif va.startswith('['):
        entries = list()
        for row in va[1: -1].split('/'):
            entries.append([translate(x.strip()) for x in row.split(',')])
        row_length = len(entries[0])
        for row in entries:
            if len(row) != row_length:
               # row.append([Number(0)] * (row_length - len(row)))
                for i in range(row_length - len(row)):
                    row.append(Number(0))
        return Matrix(entries)

    elif va.startswith('\''):
        return Text(va[1:-1])

    elif va.startswith('type('):
        m = translate(va[5:-1])
        return Text(type(m).__name__)

    elif va.startswith('z('):
        m = translate(va[2:-1])
        if isinstance(m, Error): return Error
        if isinstance(m, Number): return Vector.zero_vector(m)
        return Error('Zero Vector function not defined for ' + type(m).__name__)

    elif va.startswith('Z('):
        m = translate(va[2:-1])
        if isinstance(m, Error): return Error
        if isinstance(m, Number): return Matrix.zero_matrix(m)
        return Error('Zero Matrix function not defined for ' + type(m).__name__)

    elif va.startswith('I('):
        m = translate(va[2:-1])
        if isinstance(m, Error): return Error
        if isinstance(m, Number): return Matrix.identity_matrix(m)
        return Error('Identity Matrix function not defined for ' + type(m).__name__)

    elif va.startswith('tr('):
        m = translate(va[3:-1])
        if isinstance(m, Error): return Error
        if isinstance(m, Matrix): return Matrix.trace(m)
        return Error('Trace function not defined for ' + type(m).__name__)

    elif va.startswith('abs('):
        m = translate(va[4:-1])
        if isinstance(m, Error): return Error
        if isinstance(m, Number): return Number.absolute_value(m)
        return Error('Absolute Value function not defined for ' + type(m).__name__)

    elif va.startswith('norm('):
        m = translate(va[5:-1])
        if isinstance(m, Error): return Error
        if isinstance(m, Vector): return Vector.norm(m)
        return Error('Norm function not defined for ' + type(m).__name__)

    elif va.startswith('add('):
        lhm, rhm = general_two_function(3, va)
        if isinstance(lhm, Error): return lhm
        if isinstance(rhm, Error): return rhm
        if isinstance(lhm, Vector) and isinstance(rhm, Vector): return Vector.add_vectors(lhm, rhm)
        if isinstance(lhm, Number) and isinstance(rhm, Number): return Number.add_numbers(lhm, rhm)
        if isinstance(lhm, Matrix) and isinstance(rhm, Matrix): return Matrix.add_matrices(lhm, rhm)
        return Error('Addition function not defined for ' + type(lhm).__name__ + ' and ' + type(rhm).__name__)

    elif va.startswith('sub('):
        lhm, rhm = general_two_function(3, va)
        if isinstance(lhm, Error): return lhm
        if isinstance(rhm, Error): return rhm
        if isinstance(lhm, Number) and isinstance(rhm, Number): return Number.sub_numbers(lhm, rhm)
        if isinstance(lhm, Vector) and isinstance(rhm, Vector): return Vector.sub_vectors(lhm, rhm)
        if isinstance(lhm, Matrix) and isinstance(rhm, Matrix): return Matrix.sub_matrices(lhm, rhm)
        return Error('Addition function not defined for ' + type(lhm).__name__ + ' and ' + type(rhm).__name__)

    elif va.startswith('dot('):
        lhm, rhm = general_two_function(3, va)
        if isinstance(lhm, Error): return lhm
        if isinstance(rhm, Error): return rhm
        if isinstance(lhm, Vector) and isinstance(rhm, Vector): return Vector.dot_product(lhm, rhm)
        return Error('Dot product function not defined for ' + type(lhm).__name__ + ' and ' + type(rhm).__name__)

    elif va.startswith('mul('):
        lhm, rhm = general_two_function(3, va)
        if isinstance(lhm, Error): return lhm
        if isinstance(rhm, Error): return rhm
        if isinstance(lhm, Matrix) and isinstance(rhm, Vector): return Matrix.mul_matrix_vector(lhm, rhm)
        if isinstance(lhm, Number) and isinstance(rhm, Number): return Number.mul_numbers(lhm, rhm)
        if isinstance(lhm, Number) and isinstance(rhm, Vector): return Vector.mul_number_vector(lhm, rhm)
        if isinstance(lhm, Vector) and isinstance(rhm, Number): return Vector.mul_number_vector(rhm, lhm)
        if isinstance(lhm, Matrix) and isinstance(rhm, Matrix): return Matrix.mul_matrix_matrix(lhm, rhm)
        return Error('Multiplication function not defined for ' + type(lhm).__name__ + ' and ' + type(rhm).__name__)

    elif va.startswith('div('):
        lhm, rhm = general_two_function(3, va)
        if isinstance(lhm, Error): return lhm
        if isinstance(rhm, Error): return rhm
        if isinstance(lhm, Number) and isinstance(rhm, Number): return Number.div_numbers(lhm, rhm)

    elif va.startswith('pow('):
        lhm, rhm = general_two_function(3, va)
        if isinstance(lhm, Error): return lhm
        if isinstance(rhm, Error): return rhm
        if isinstance(lhm, Number) and isinstance(rhm, Number): return Number.pow_numbers(lhm, rhm)
        return Error('Power function not defined for ' + type(lhm).__name__ + ' and ' + type(rhm).__name__)

    elif va.startswith('comp('):
        lhm, rhm = general_two_function(4, va)
        if isinstance(lhm, Error): return lhm
        if isinstance(rhm, Error): return rhm
        if isinstance(lhm, Vector) and isinstance(rhm, Number): return Vector.component(lhm, rhm)
        return Error('Component function not defined for ' + type(lhm).__name__ + ' and ' + type(rhm).__name__)

    elif va.startswith('latex('):
        lhm, rhm = general_two_function(5, va)
        if isinstance(lhm, Error): return lhm
        if isinstance(rhm, Error): return rhm
        if isinstance(lhm, Matrix) and isinstance(rhm, Text): return Matrix.latex(lhm, rhm)
        return Error('Latex function not defined for ' + type(lhm).__name__ + ' and ' + type(rhm).__name__)

    elif va.startswith('entry('):
        m1, m2, m3 = general_three_function(5, va)
        if isinstance(m1, Error): return m1
        if isinstance(m2, Error): return m2
        if isinstance(m3, Error): return m3
        if isinstance(m1, Matrix) and isinstance(m2, Number) and isinstance(m3, Number): return Matrix.entry(m1, m2, m3)

    return Error('Cannot translate \'' + va + '\' into an object')


def create(ln):
    # ln: [id] = object
    new_id = ln[:ln.index('=')].strip()
    if ids.__contains__(new_id):
        return Error(new_id + ' already exists')

    obj = translate(ln[ln.index('=') + 1:].strip())
    ids.append(new_id)
    data.append(obj)

    return obj


def help():
    for line in open('help.txt', 'r').readlines():
        print(line, end='')


def info():
    print('Toggle print create:', toggle_print_create)
    print('Data size:', len(ids))
    print('History size:', len(history))


def meta_run():
    temp_cmds = list()
    while True:
        temp_cmd = input()
        if temp_cmd == 'q':
            for line in temp_cmds:
                run(line)
            return
        else:
            temp_cmds.append(temp_cmd)


def run(ln):
    global toggle_print_create

    if ln.startswith('#') or len(ln) == 0:
        return
    elif ln == 'q':
        quit(0)
    elif ln == 'help':
        help()
    elif ln == 'i':
        info()
    elif ln == 'c':
        ids.clear()
        data.clear()
        history.clear()
    elif ln == 'h':
        for i in history: print(i)
    elif ln == 'toggle':
        toggle_print_create = not toggle_print_create
    elif ln == 'run':
        meta_run()

    elif ln.__contains__('='):
        if not toggle_print_create:
            result = create(ln)
            if isinstance(result, Error):
                print(result.present())
        else:
            print(create(ln).present())

    else:
        print(translate(ln).present())


while True:
    cmd = input()

    if cmd == 'q':
        exit(0)

    if cmd not in ['h', 'help', 'c', 'q', 'i']: history.append(cmd)
    run(cmd)
