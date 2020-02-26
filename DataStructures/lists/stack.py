# Python list append and pop provides the expected operations

# Check parentheses
def check_parentheses(data):
    stack = []
    for c in data:
        if c == '(': stack.append(c)
        elif c == ')':
            if len(stack) == 0: return False
            stack.pop()
    return len(stack) == 0

print(check_parentheses('(())')) # True
print(check_parentheses('()()')) # True
print(check_parentheses('(()'))  # False
print(check_parentheses('())'))  # False
