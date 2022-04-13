from pylinal import Matrix, Vector


A = Matrix([
    [-1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])
v = Vector([3, -1, 2])

reflection = lambda x: A @ x
motion = lambda x: x + v

affine = lambda x: motion(reflection(x))

x = Vector([1, 1, 1])
assert affine(x) == A @ x + v


