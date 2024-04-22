class TreeNode {
  constructor(operator) {
    this.operator = operator;
    this.left = null;
    this.right = null;
  }
}

const buildExpressionTree = (expression) => {
  const parts = expression.split(" ").reverse(); // Reverse the expression to process from right to left
  const stack = [];
  console.log(parts);
  for (let i = 0; i < parts.length; i++) {
    const current = parts[i];

    if (["+", "-", "*", "/"].includes(current)) {
      const newNode = new TreeNode(current);
      newNode.left = stack.pop();
      newNode.right = stack.pop();
      stack.push(newNode);
    } else {
      stack.push(new TreeNode(parseFloat(current)));
    }
  }

  return stack[0];
};

const evaluateExpressionTree = (root) => {
  if (!root) return 0;

  if (!root.left && !root.right) {
    return root.operator;
  }

  const leftOperand = evaluateExpressionTree(root.left);
  const rightOperand = evaluateExpressionTree(root.right);

  switch (root.operator) {
    case "+":
      return leftOperand + rightOperand;
    case "-":
      return leftOperand - rightOperand;
    case "*":
      return leftOperand * rightOperand;
    case "/":
      // Handle edge cases of division by zero.
      if (rightOperand === 0) {
        throw new Error("Division by zero");
      }
      return leftOperand / rightOperand;
    default:
      // Invalid operator
      throw new Error("Invalid operator");
  }
};

const expression = "* + 3 4 5";
const tree = buildExpressionTree(expression);
console.log(tree);
console.log(evaluateExpressionTree(tree)); // Output: 35
