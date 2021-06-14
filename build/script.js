var _a, _b, _c;
import { Tree } from "./tree.js";
var tree = new Tree();
var timeout = undefined;
var canvas = document.getElementById("canvas");
var notify_div = document.getElementById("notify");
var main_input = document.getElementById("value");
var btn_push = document.getElementById("push_value");
var btn_pop = document.getElementById("pop_value");
var table_node = (_a = document.getElementById("node-desc")) === null || _a === void 0 ? void 0 : _a.cloneNode(true);
var table_duo_node = (_b = document
    .getElementById("duo-node-desc")) === null || _b === void 0 ? void 0 : _b.cloneNode(true);
(_c = document.getElementById("duo-node-desc")) === null || _c === void 0 ? void 0 : _c.remove();
var ctx = canvas.getContext("2d");
ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;
ctx.font = "15px Roboto";
function node_draw(node) {
    var value = node.value.toString();
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
    ctx.fillText(value, node.position.x - ctx.measureText(value).width / 2, node.position.y + 4);
}
function draw(root) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    if (root)
        node_draw(root);
}
function notify(msg) {
    clearTimeout(timeout);
    var text = notify_div.children[0];
    text.innerText = msg;
    notify_div.style.display = "block";
    timeout = setTimeout(function () {
        notify_div.style.display = "none";
    }, 7000);
}
globalThis.myClose = function (e) {
    e.parentElement.style.display = "none";
};
if (main_input) {
    main_input.addEventListener("keyup", function (event) {
        var _a;
        var key = event.key;
        if (key === "Enter" && main_input.value) {
            var input_readonly = main_input.cloneNode();
            input_readonly.setAttribute("readonly", "");
            input_readonly.removeAttribute("id");
            input_readonly.removeAttribute("autofocus");
            (_a = main_input.parentElement) === null || _a === void 0 ? void 0 : _a.insertBefore(input_readonly, main_input);
            main_input.value = "";
        }
    });
}
btn_push.onclick = function () {
    this.blur();
    var lote = document.getElementById("lote");
    var value = lote.value;
    lote.value = "";
    if (value) {
        var values = value.split(",");
        values.forEach(function (value_) {
            value = Number(value_);
            if (value) {
                res = tree.push(value);
                if (!res) {
                    notify("O nó " + value + " já está na árvore.");
                }
            }
        });
    }
    draw(tree.root);
    var inputs = document.getElementsByName("value");
    var res = false;
    while (inputs[0]) {
        value = Number(inputs[0].value);
        if (value) {
            res = tree.push(value);
            console.info("Inserido: ", res);
            if (res) {
                draw(tree.root);
            }
            else {
                notify("O nó " + value + " já está na árvore.");
            }
        }
        if (inputs[0] !== main_input) {
            inputs[0].remove();
        }
        else {
            inputs[0].value = "";
            break;
        }
    }
};
btn_pop.onclick = function () {
    this.blur();
    var input = document.getElementById("pop_input");
    var value = Number(input.value);
    if (value) {
        var res = tree.pop(value);
        if (!res) {
            notify("O n\u00F3 " + value + " n\u00E3o foi removido.");
        }
        draw(tree.root);
    }
    input.value = "";
};
