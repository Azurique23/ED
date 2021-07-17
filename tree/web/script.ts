// @Marcos Pacheco
// @Danilo Brandão

const tree = new Tree();

var timeout: number | undefined = undefined;

// PEGANDO OS ELEMENTOS DO DOM
const canvas = document.getElementById("canvas") as HTMLCanvasElement;
const notify_div = document.getElementById("notify") as HTMLDivElement;
const main_input = document.getElementById("value") as HTMLInputElement;
const btn_push = document.getElementById("push_value") as HTMLButtonElement;
const btn_pop = document.getElementById("pop_value") as HTMLButtonElement;
const btn_search = document.getElementById("search_btn") as HTMLButtonElement;
const btn_search_duo = document.getElementById(
  "search_duo_btn"
) as HTMLButtonElement;
const div_tbs = document.getElementById("desc") as HTMLDivElement;
const table_node = document.getElementById("node-desc")?.cloneNode(true);
const table_duo_node = document
  .getElementById("duo-node-desc")
  ?.cloneNode(true);
document.getElementById("duo-node-desc")?.remove();

// CANVAS
const ctx = canvas.getContext("2d") as CanvasRenderingContext2D;
ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;
ctx.font = "15px Roboto";

//  FUNÇÕES PARA MANIPULZAÇÃO DO DOM E DA ÁRVORE BINÁRIA.
function updateTreeDesc(tree: Tree): void {
  (document.getElementById("lenght") as HTMLSpanElement).innerText =
    "" + tree.lenght;
  (document.getElementById("height") as HTMLSpanElement).innerText = String(
    tree.height
  );
}

function notify(msg: string): void {
  clearTimeout(timeout);
  let text = notify_div.children[0] as HTMLParagraphElement;
  text.innerText = msg;
  notify_div.style.display = "block";
  timeout = setTimeout(() => {
    notify_div.style.display = "none";
  }, 7000);
}

var myClose = (e: HTMLElement): void => {
  e.parentElement!.style.display = "none";
};

if (main_input) {
  main_input.addEventListener("keyup", (event) => {
    var key = event.key;
    if (key === "Enter" && main_input.value) {
      let input_readonly = main_input.cloneNode() as HTMLInputElement;
      input_readonly.setAttribute("readonly", "");
      input_readonly.removeAttribute("id");
      input_readonly.removeAttribute("autofocus");
      main_input.parentElement?.insertBefore(input_readonly, main_input);
      main_input.value = "";
    }
  });
}

btn_push.onclick = function () {
  (this as HTMLButtonElement).blur();

  const lote = document.getElementById("lote") as HTMLInputElement;
  let value: string | undefined | number = lote.value;
  lote.value = "";
  if (value) {
    let values = (value as string).split(";");
    values.forEach((value_) => {
      value = Number(value_);
      if (value) {
        res = tree.push(value);
        if (!res) {
          notify("O nó " + value + " já está na árvore.");
        }
      } else {
        notify(`A entrada ${value_} é inválivda.`);
      }
    });
  }
  tree.draw(ctx);

  let inputs = document.getElementsByName("value");

  let res = false;
  while (inputs[0]) {
    value = Number((inputs[0] as HTMLInputElement).value);
    if (value) {
      res = tree.push(value);
      // console.info("Inserido: ", res);
      if (res) {
        tree.draw(ctx);
      } else {
        notify("O nó " + value + " já está na árvore.");
      }
    }
    if (inputs[0] !== main_input) {
      inputs[0].remove();
    } else {
      (inputs[0] as HTMLInputElement).value = "";
      break;
    }
  }

  updateTreeDesc(tree);
};

btn_pop.onclick = function () {
  (this as HTMLButtonElement).blur();

  let input = document.getElementById("pop_input") as HTMLInputElement;

  const value = Number(input.value);
  if (value) {
    let res = tree.pop(value);

    if (!res) {
      notify(`O nó ${value} não foi removido.`);
    }
    tree.draw(ctx);
  }
  updateTreeDesc(tree);
  input.value = "";
};

function descNode(node: TreeNode): void {
  const table = table_node?.cloneNode(true) as HTMLTableElement;

  let dad = node.dad ? node.dad.value : 0;
  let right = node.right ? node.right.value : 0;
  let left = node.left ? node.left.value : 0;
  const tbody = table.children[0] as HTMLTableElement;
  tbody.children[1].children[1].innerHTML = String(node.value);
  tbody.children[1].children[3].innerHTML = String(node.level);
  tbody.children[2].children[1].innerHTML = String(node.degree);
  tbody.children[2].children[3].innerHTML = String(dad);
  tbody.children[3].children[1].innerHTML = String(right);
  tbody.children[3].children[3].innerHTML = String(left);

  div_tbs.children[1].remove();
  div_tbs.appendChild(table);
}

function descNodeDuo(nodea: TreeNode, nodeb: TreeNode): void {
  const table = table_duo_node?.cloneNode(true) as HTMLTableElement;

  let dada = nodea.dad ? nodea.dad.value : 0;
  let righta = nodea.right ? nodea.right.value : 0;
  let lefta = nodea.left ? nodea.left.value : 0;
  let dadb = nodeb.dad ? nodeb.dad.value : 0;
  let rightb = nodeb.right ? nodeb.right.value : 0;
  let leftb = nodeb.left ? nodeb.left.value : 0;
  const tbody = table.children[0] as HTMLTableElement;

  tbody.children[1].children[1].innerHTML = String(nodea.value);
  tbody.children[1].children[2].innerHTML = String(nodeb.value);

  tbody.children[1].children[4].innerHTML = String(nodea.level);
  tbody.children[1].children[5].innerHTML = String(nodeb.level);

  tbody.children[2].children[1].innerHTML = String(nodea.degree);
  tbody.children[2].children[2].innerHTML = String(nodeb.degree);

  tbody.children[2].children[4].innerHTML = String(dada);
  tbody.children[2].children[5].innerHTML = String(dadb);

  tbody.children[3].children[1].innerHTML = String(righta);
  tbody.children[3].children[2].innerHTML = String(rightb);

  tbody.children[3].children[4].innerHTML = String(lefta);
  tbody.children[3].children[5].innerHTML = String(leftb);

  div_tbs.children[1].remove();
  div_tbs.appendChild(table);
}

btn_search.onclick = function (this: HTMLButtonElement) {
  let input = document.getElementById("search_value") as HTMLInputElement;
  const value = Number(input.value);
  if (value) {
    const node = tree.search(value) as TypeNode;
    if (node) {
      descNode(node);
      tree.searchDraw(node, tree.root as TreeNode, ctx);
    } else {
      notify(`O nó ${value} não foi encontrado na árvore.`);
    }
  } else {
    notify("Impossivel de encontra o nó com um valor desse.");
  }
  this.blur();
  // input.value = "";
};

btn_search_duo.onclick = function (this: HTMLButtonElement) {
  let a = document.getElementById("value-a") as HTMLInputElement;
  let b = document.getElementById("value-b") as HTMLInputElement;
  let valuea = Number(a.value);
  let valueb = Number(b.value);

  if (valuea && valueb) {
    const [nodea, nodeb, nodec] = tree.search(valuea, valueb) as [
      TypeNode,
      TypeNode,
      TypeNode
    ];
    if (nodea && nodeb && nodec) {
      if (nodea === nodec) {
        tree.searchDraw(nodeb, nodec, ctx);
      } else if (nodeb === nodec) {
        tree.searchDraw(nodea, nodec, ctx);
      } else {
        tree.searchDraw(nodea, nodec, ctx, true, true);
        tree.searchDraw(nodeb, nodec, ctx, false);
      }
      descNodeDuo(nodea, nodeb);
    } else if (!nodea && nodeb) {
      notify(`O nó A:${valuea} não foi encontrado.`);
    } else if (!nodeb && nodea) {
      notify(`O nó B:${valueb} não foi encontrado.`);
    } else {
      notify(`O nó A:${valuea} e B:${valueb} não foram encontrado.`);
    }
  } else {
    notify("Entrada ou entradas inválidas.");
  }
  this.blur();
};

updateTreeDesc(tree);

// canvas.onmousemove = function(e){
//   let rect = (this as HTMLCanvasElement).getBoundingClientRect()
//   let scaleX = canvas.width / rect.width, scaleY = canvas.height / rect.height;

//   let x = (e.clientX - rect.left)*scaleX
//   let y = (e.clientY -rect.top)*scaleY

//   console.log(x,y)
// }
