export type TypeNode = TreeNode | undefined;

export class TreeNode {
  value: number;
  level: number;
  degree: number;
  dad: TypeNode;
  right: TypeNode;
  left: TypeNode;
  position: { x: number; y: number };

  constructor(value: number) {
    this.value = value;
    this.level = 0;
    this.degree = 0;
    this.dad = undefined;
    this.right = undefined;
    this.left = undefined;
    this.position = { x: 0, y: 0 };
  }
}

export class Tree {
  root: TypeNode;
  lenght: number;
  height: number;
  biggest: number;
  lowest: number;
  offsetX: number;
  offsetY: number;

  constructor() {
    this.root = undefined;
    this.lenght = 0;
    this.height = 0;
    this.biggest = 0;
    this.lowest = 0;
    this.offsetX = 40;
    this.offsetY = 64;
  }
  push(value: number): boolean {
    const offsetX = this.offsetX;
    const offsetY = this.offsetY;

    function search(root: TreeNode, value: number): TypeNode {
      function searchRight(node: TreeNode, value: number): TypeNode {
        if (node.value == value) {
          return undefined;
        }
        if (node.value > value) {
          if (node.right) return searchRight(node.right, value);
        } else {
          if (node.left) {
            let res = searchRight(node.left, value);
            if (res) {
              node.position.x -= offsetX;
              if (node.right) Tree.updateX(node.right, -offsetX);
            }
            return res;
          }
          node.position.x -= offsetX;
          if (node.right) Tree.updateX(node.right, -offsetX);
        }
        return node;
      }
      function searchLeft(node: TreeNode, value: number): TypeNode {
        if (node.value == value) {
          return undefined;
        }
        if (node.value > value) {
          if (node.right) {
            let res = searchLeft(node.right, value);
            if (res) {
              node.position.x += offsetX;
              if (node.left) Tree.updateX(node.left, offsetX);
            }
            return res;
          }
          node.position.x += offsetX;
          if (node.left) Tree.updateX(node.left, offsetX);
        } else {
          if (node.left) return searchLeft(node.left, value);
        }
        return node;
      }

      if (root.value > value){
        if (root.right)return searchRight(root.right, value)
      }else{
        if (root.left)return searchLeft(root.left, value)
      }

      return root;
    }

    if (this.root) {
      const dad = search(this.root, value);

      if (dad) {
        const node = new TreeNode(value);

        if (dad.value > value) {
          dad.right = node;
          node.position.x = dad.position.x - offsetX;
        } else {
          dad.left = node;
          node.position.x = dad.position.x + offsetX;
        }
        node.position.y = dad.position.y + offsetY;

        dad.degree += 1;

        node.dad = dad;
        node.level = dad.level + 1;

        this.lenght++;
        if (value > this.biggest) this.biggest = value;
        if (value < this.lowest) this.lowest = value;
        if (this.height <= node.level) this.height = node.level + 1;

        return true;
      }
      return false;
    } else {
      this.root = new TreeNode(value);
      this.height = 1;
      this.lenght++;
      this.biggest++;
      this.lowest = value;
      this.biggest = value;
      this.root.position.x = window.innerWidth / 2;
      this.root.position.y = 27;
      return true;
    }
  }

  travel() {
    function travel(node: TreeNode): void {
      console.log(
        `Value: ${node.value}, Grau: ${node.degree}, Level: ${node.level}`
      );
      console.log(node.position);
      if (node.right) travel(node.right);
      if (node.left) travel(node.left);
    }
    if (this.root) travel(this.root);
  }

  static updateX(node: TreeNode, offset: number, right: boolean = true): void {
    function travel(node: TreeNode): void {
      node.position.x += offset;
      if (node.right) travel(node.right);
      if (node.left) travel(node.left);
    }

    travel(node);
  }
}
