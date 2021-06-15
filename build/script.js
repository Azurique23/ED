var _a, _b, _c;
var tree = new Tree();
var timeout = undefined;
var canvas = document.getElementById("canvas");
var notify_div = document.getElementById("notify");
var main_input = document.getElementById("value");
var btn_push = document.getElementById("push_value");
var btn_pop = document.getElementById("pop_value");
var btn_search = document.getElementById("search_btn");
var btn_search_duo = document.getElementById("search_duo_btn");
var div_tbs = document.getElementById("desc");
var table_node = (_a = document.getElementById("node-desc")) === null || _a === void 0 ? void 0 : _a.cloneNode(true);
var table_duo_node = (_b = document
    .getElementById("duo-node-desc")) === null || _b === void 0 ? void 0 : _b.cloneNode(true);
(_c = document.getElementById("duo-node-desc")) === null || _c === void 0 ? void 0 : _c.remove();
var ctx = canvas.getContext("2d");
ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;
ctx.font = "15px Roboto";
function updateTreeDesc(tree) {
    document.getElementById("lenght").innerText =
        "" + tree.lenght;
    document.getElementById("height").innerText = String(tree.height);
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
var myClose = function (e) {
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
        var values = value.split(";");
        values.forEach(function (value_) {
            value = Number(value_);
            if (value) {
                res = tree.push(value);
                if (!res) {
                    notify("O nó " + value + " já está na árvore.");
                }
            }
            else {
                notify("A entrada " + value_ + " \u00E9 inv\u00E1livda.");
            }
        });
    }
    tree.draw(ctx);
    var inputs = document.getElementsByName("value");
    var res = false;
    while (inputs[0]) {
        value = Number(inputs[0].value);
        if (value) {
            res = tree.push(value);
            if (res) {
                tree.draw(ctx);
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
    updateTreeDesc(tree);
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
        tree.draw(ctx);
    }
    updateTreeDesc(tree);
    input.value = "";
};
function descNode(node) {
    var table = table_node === null || table_node === void 0 ? void 0 : table_node.cloneNode(true);
    var dad = node.dad ? node.dad.value : 0;
    var right = node.right ? node.right.value : 0;
    var left = node.left ? node.left.value : 0;
    var tbody = table.children[0];
    tbody.children[1].children[1].innerHTML = String(node.value);
    tbody.children[1].children[3].innerHTML = String(node.level);
    tbody.children[2].children[1].innerHTML = String(node.degree);
    tbody.children[2].children[3].innerHTML = String(dad);
    tbody.children[3].children[1].innerHTML = String(right);
    tbody.children[3].children[3].innerHTML = String(left);
    div_tbs.children[1].remove();
    div_tbs.appendChild(table);
}
function descNodeDuo(nodea, nodeb) {
    var table = table_duo_node === null || table_duo_node === void 0 ? void 0 : table_duo_node.cloneNode(true);
    var dada = nodea.dad ? nodea.dad.value : 0;
    var righta = nodea.right ? nodea.right.value : 0;
    var lefta = nodea.left ? nodea.left.value : 0;
    var dadb = nodeb.dad ? nodeb.dad.value : 0;
    var rightb = nodeb.right ? nodeb.right.value : 0;
    var leftb = nodeb.left ? nodeb.left.value : 0;
    var tbody = table.children[0];
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
btn_search.onclick = function () {
    var input = document.getElementById("search_value");
    var value = Number(input.value);
    if (value) {
        var node = tree.search(value);
        if (node) {
            descNode(node);
            tree.searchDraw(node, tree.root, ctx);
        }
        else {
            notify("O n\u00F3 " + value + " n\u00E3o foi encontrado na \u00E1rvore.");
        }
    }
    else {
        notify("Impossivel de encontra o nó com um valor desse.");
    }
    this.blur();
};
btn_search_duo.onclick = function () {
    var a = document.getElementById("value-a");
    var b = document.getElementById("value-b");
    var valuea = Number(a.value);
    var valueb = Number(b.value);
    if (valuea && valueb) {
        var _a = tree.search(valuea, valueb), nodea = _a[0], nodeb = _a[1], nodec = _a[2];
        if (nodea && nodeb && nodec) {
            if (nodea === nodec) {
                tree.searchDraw(nodeb, nodec, ctx);
            }
            else if (nodeb === nodec) {
                tree.searchDraw(nodea, nodec, ctx);
            }
            else {
                tree.searchDraw(nodea, nodec, ctx, true, true);
                tree.searchDraw(nodeb, nodec, ctx, false);
            }
            descNodeDuo(nodea, nodeb);
        }
        else if (!nodea && nodeb) {
            notify("O n\u00F3 A:" + valuea + " n\u00E3o foi encontrado.");
        }
        else if (!nodeb && nodea) {
            notify("O n\u00F3 B:" + valueb + " n\u00E3o foi encontrado.");
        }
        else {
            notify("O n\u00F3 A:" + valuea + " e B:" + valueb + " n\u00E3o foram encontrado.");
        }
    }
    else {
        notify("Entrada ou entradas inválidas.");
    }
    this.blur();
};
updateTreeDesc(tree);
