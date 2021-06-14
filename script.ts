import { Tree, TreeNode, TypeNode } from "./tree.js";

declare namespace globalThis{
  var myClose: (e: HTMLElement) => void
}

const tree = new Tree();
var timeout: number| undefined = undefined 
const canvas = document.getElementById("canvas") as HTMLCanvasElement;
const notify_div = document.getElementById("notify") as HTMLDivElement;
const main_input = document.getElementById("value") as HTMLInputElement;
const btn_push = document.getElementById("push_value") as HTMLButtonElement;
const btn_pop = document.getElementById("pop_value") as HTMLButtonElement;
const table_node = document.getElementById("node-desc")?.cloneNode(true);
const table_duo_node = document
  .getElementById("duo-node-desc")
  ?.cloneNode(true);
document.getElementById("duo-node-desc")?.remove();

// canvas.onmousemove = function(e){
//   let rect = (this as HTMLCanvasElement).getBoundingClientRect()
//   let scaleX = canvas.width / rect.width, scaleY = canvas.height / rect.height;

//   let x = (e.clientX - rect.left)*scaleX
//   let y = (e.clientY -rect.top)*scaleY

//   console.log(x,y)
// }

const ctx = canvas.getContext("2d") as CanvasRenderingContext2D;

ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;
ctx.font = "15px Roboto";

function node_draw(node: TreeNode): void {
  let value = node.value.toString();
  // console.log(node)
  if (node.right) {
    ctx.beginPath();
    ctx.lineWidth = 1.4;
    ctx.lineTo(node.position.x, node.position.y);
    ctx.lineTo(node.right.position.x, node.right.position.y);
    ctx.stroke();
    node_draw(node.right);
  }

  if (node.left) {
    ctx.beginPath();
    ctx.lineWidth = 1.4;
    ctx.lineTo(node.position.x, node.position.y);
    ctx.lineTo(node.left.position.x, node.left.position.y);
    ctx.stroke();
    node_draw(node.left);
  }

  ctx.beginPath();
  ctx.fillStyle = "black";
  ctx.arc(node.position.x, node.position.y, 25, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.beginPath();
  ctx.fillStyle = "white";
  ctx.fillText(
    value,
    node.position.x - ctx.measureText(value).width / 2,
    node.position.y + 4
  );
}
function draw(root: TypeNode) {
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

  if (root) node_draw(root);
}

function notify(msg: string): void {
  clearTimeout(timeout)
  let text = notify_div.children[0] as HTMLParagraphElement;
  text.innerText = msg;
  notify_div.style.display = "block";
  timeout = setTimeout(()=>{
    notify_div.style.display = "none"
  }, 7000)
}
globalThis.myClose = (e: HTMLElement): void => {
  e.parentElement!.style.display = "none";
}

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
    let values = (value as string).split(",");
    values.forEach((value_) => {
      value = Number(value_);
      if (value) {
        res = tree.push(value);
        if(!res){
          notify("O nó "+value+" já está na árvore.")
        }
      }
    });
  }
  draw(tree.root);

  let inputs = document.getElementsByName("value");

  let res = false;
  while (inputs[0]) {
    value = Number((inputs[0] as HTMLInputElement).value);
    if (value) {
      res = tree.push(value);
      console.info("Inserido: ", res);
      if (res) {
        draw(tree.root);
      }else{
        notify("O nó "+value+" já está na árvore.")
      }
    }
    if (inputs[0] !== main_input) {
      inputs[0].remove();
    } else {
      (inputs[0] as HTMLInputElement).value = "";
      break;
    }
  }
};

btn_pop.onclick = function () {
  (this as HTMLButtonElement).blur();

  let input = document.getElementById("pop_input") as HTMLInputElement;

  const value = Number(input.value);
  if (value) {
    let res = tree.pop(value);

    if (!res) {
      notify(`O nó ${value} não foi removido.`)
    }
    draw(tree.root);
  }

  input.value = "";
};
