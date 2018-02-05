"""
This is a test file to evaluate development tools
"""


def hello_world(x: int) -> str:
    return str(x) + str(x)


if __name__ == '__main__':
    print("Hello world, {0}".format(hello_world(7)))
