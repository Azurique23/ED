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

      if (root.value > value) {
        if (root.right) return searchRight(root.right, value);
      } else {
        if (root.left) return searchLeft(root.left, value);
      }
      if (root.value !== value) {
        return root;
      }
      return undefined;
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

  pop(value: number): boolean {
    const offsetX = this.offsetX;
    const offsetY = this.offsetY;

    function search(root: TreeNode, value: number): [TypeNode, number] {
      function searchRight(node: TreeNode, value: number): [TypeNode, number] {
        if (node.value == value) {
          return [node, 0];
        }
        if (node.value > value) {
          if (node.right) return searchRight(node.right, value);
        } else {
          if (node.left) {
            let res = searchRight(node.left, value);
            if (res) {
              res[1] = offsetX;
              node.position.x += offsetX;
              if (node.right) Tree.updateX(node.right, offsetX);
            }
            return res;
          }
        }
        return [undefined, 0];
      }
      function searchLeft(node: TreeNode, value: number): [TypeNode, number] {
        if (node.value == value) {
          return [node, 0];
        }
        if (node.value > value) {
          if (node.right) {
            let res = searchLeft(node.right, value);
            if (res) {
              res[1] = -offsetX;
              node.position.x -= offsetX;
              if (node.left) Tree.updateX(node.left, -offsetX);
            }
            return res;
          }
        } else {
          if (node.left) return searchLeft(node.left, value);
        }
        return [undefined, 0];
      }

      if (root.value == value) return [root, 0];

      if (root.value > value) {
        if (root.right) return searchRight(root.right, value);
      } else {
        if (root.left) return searchLeft(root.left, value);
      }

      return [undefined, 0];
    }
    function travelRight(node: TreeNode): TreeNode {
      if (node.right) {
        return travelRight(node.right);
      }
      return node;
    }

    if (!this.root) {
      return false;
    }

    let [node, offset] = search(this.root as TreeNode, value);

    if (node) {
      if (node.degree === 0) {
        if (node.dad) {
          if (node.dad.right === node) {
            node.dad.right = undefined;
          } else {
            node.dad.left = undefined;
          }
          node.dad.degree -= 1;
        } else {
          this.root = undefined;
        }
      } else if (node.degree === 1) {
        const nodereplace = node.right ? node.right : (node.left as TreeNode);

        if (node.dad) {
          nodereplace.dad = node.dad;

          if (node.dad.right == node) {
            if (node.right == nodereplace) {
              offset = node.dad.position.x - node.position.x;
            }

            node.dad.right = nodereplace;
          } else {
            if (node.left == nodereplace) {
              offset = node.dad.position.x - node.position.x;
            }
            node.dad.left = nodereplace;
          }
        } else {
          offset = node.position.x - nodereplace.position.x;
          nodereplace.dad = undefined;
          this.root = nodereplace;
        }
        Tree.updateX(nodereplace, offset);
        nodereplace.level = node.level;
        console.log(nodereplace);
      } else {
        let nodereplace = travelRight(node.left as TreeNode);

        nodereplace.level = node.level;
        if (nodereplace === node.left) {
          offset = node.position.x - nodereplace.position.x;
          if (this.root.value > value) {
            offset = 0;
            Tree.updateX(node.right as TreeNode, offsetX);
          }
          Tree.updateX(nodereplace, offset);

          if (node.right) {
            node.right.dad = nodereplace;
            nodereplace.right = node.right;
          }
          nodereplace.degree = nodereplace.left ? 2 : 1;

          if (node.dad) {
            if (node.dad.right === node) {
              node.dad.right = nodereplace;
            } else {
              node.dad.left = nodereplace;
            }
          } else {
            this.root = nodereplace;
          }
          nodereplace.dad = node.dad;
        } else {
          if (nodereplace.left) {
            nodereplace.dad!.right = nodereplace.left;
            nodereplace.left!.dad = nodereplace.dad;
          } else {
            nodereplace.dad!.right = undefined;
            nodereplace.dad!.degree--;
          }

          nodereplace.degree = node.degree;

          node.right!.dad = nodereplace;
          node.left!.dad = nodereplace;

          nodereplace.right = node.right;
          nodereplace.left = node.left;
          nodereplace.dad = node.dad;

          if (node.dad) {
            if (node.dad.right === node) {
              node.dad.right = nodereplace;
            } else {
              node.dad.left = nodereplace;
            }
          } else {
            this.root = nodereplace;
          }

          if (this.root.value > value && this.root != nodereplace) {
            Tree.updateX(nodereplace.right as TreeNode, offsetX);
          } else {
            offset = -offsetX;
            nodereplace.position.x -= offsetX;
            Tree.updateX(nodereplace.left as TreeNode, offset);
          }
        }
      }

      this.lenght -= 1;
      this.updateTree();
      return true;
    }

    return false;
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

  search(value: number, b: number | undefined = undefined): TypeNode[] {
    function search(node: TreeNode, value: number): TypeNode {
      if (node.value == value) {
        return node;
      }
      if (node.value > value) {
        if (node.right) return search(node.right, value);
      } else {
        if (node.left) return search(node.left, value);
      }
      return undefined;
    }

    function searchAB(node: TreeNode, a: number, b: number): TypeNode[] {
      if (
        node.value > a == node.value > b &&
        !(node.value == a || node.value == b)
      ) {
        if (node.value > a) {
          if (node.right) return searchAB(node.right, a, b);
        } else {
          if (node.left) return searchAB(node.left, a, b);
        }
        return [undefined, undefined];
      } else if (node.value == a) {
        return [node, search(node, b)]
      } else if (node.value == b) {
        return [search(node, a), node]
      } else {
        return [search(node, a), search(node, b)]
      }
    }

    if (!this.root) {
      return [undefined, undefined];
    }

    if (b) {
      return searchAB(this.root, value, b);
    } else {
      return [search(this.root, value), undefined];
    }
  }

  updateTree() {
    const offsetY = this.offsetY;

    function travel(node: TreeNode, tree: Tree): void {
      node.position.y = offsetY * node.level + 27;

      if (node.right) {
        node.right.level = node.level + 1;
        travel(node.right, tree);
      }
      if (node.left) {
        node.left.level = node.level + 1;
        travel(node.left, tree);
      }

      if (node.level >= tree.height) tree.height = node.level + 1;
      if (node.value > tree.biggest) tree.biggest = node.value;
      if (node.value < tree.lowest) tree.lowest = node.value;
    }

    this.height = 0;
    this.lowest = 0;
    this.biggest = 0;

    if (this.root) {
      this.lowest = this.root.value;
      this.biggest = this.root.value;
      this.root.level = 0;
      travel(this.root, this);
    }
  }

  static updateX(node: TreeNode, offset: number): void {
    function travel(node: TreeNode): void {
      node.position.x += offset;
      if (node.right) travel(node.right);
      if (node.left) travel(node.left);
    }

    travel(node);
  }
}
