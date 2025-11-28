/*ALERTAS*/
function showError(msg) {
    const a = document.getElementById("alertaError");
    a.innerText = msg;
    a.style.display = "block";
    document.getElementById("alertaOk").style.display = "none";
}

function showOk(msg) {
    const a = document.getElementById("alertaOk");
    a.innerText = msg;
    a.style.display = "block";
    document.getElementById("alertaError").style.display = "none";
}

function clearAlerts() {
    document.getElementById("alertaError").style.display = "none";
    document.getElementById("alertaOk").style.display = "none";
}

/*INPUTS*/
function markInputError(input, msg) {
    input.classList.add("input-error");
    const m = document.createElement("div");
    m.classList.add("error-msg");
    m.innerText = msg;

    if (input.nextSibling)
        input.parentNode.insertBefore(m, input.nextSibling);
    else
        input.parentNode.appendChild(m);
}

function clearInputErrors() {
    document.querySelectorAll(".error-msg").forEach(e => e.remove());
    document.querySelectorAll(".fila-matriz input").forEach(i => i.classList.remove("input-error"));
}

/*MOSTRAR U OCULTAR FILA/COLUMNA EN 4×4*/
function toggleFilaColumna() {
    const tam = Number(document.getElementById("tamano").value);
    const metodo = document.getElementById("metodo").value;

    const row = document.getElementById("filaColumnaRow");
    row.style.display = (tam === 4 && metodo === "cofactores")
        ? "flex"
        : "none";
}

/*MÉTODOS SEGÚN TAMAÑE*/
function actualizarMetodos() {
    const tam = Number(document.getElementById("tamano").value);
    const metodoSel = document.getElementById("metodo");

    metodoSel.innerHTML = "";

    if (tam === 2) {
        metodoSel.innerHTML += `<option value="cofactores">Cofactores (2×2)</option>`;
    }
    if (tam === 3) {
        metodoSel.innerHTML += `<option value="sarrus">Sarrus</option>`;
        metodoSel.innerHTML += `<option value="cofactores">Cofactores</option>`;
        metodoSel.innerHTML += `<option value="gauss">Gauss</option>`;
    }
    if (tam === 4) {
        metodoSel.innerHTML += `<option value="cofactores">Cofactores</option>`;
        metodoSel.innerHTML += `<option value="gauss">Gauss</option>`;
    }

    toggleFilaColumna();
}

/*GENERAR MATRIZ*/
function generarMatriz() {
    const tam = Number(document.getElementById("tamano").value);
    const cont = document.getElementById("matrizInputs");

    cont.innerHTML = "";

    for (let f = 0; f < tam; f++) {
        const filaDiv = document.createElement("div");
        filaDiv.classList.add("fila-matriz");

        for (let c = 0; c < tam; c++) {
            const input = document.createElement("input");
            input.type = "text";
            input.id = `c${f}_${c}`;
            input.placeholder = "0";
            filaDiv.appendChild(input);
        }

        cont.appendChild(filaDiv);
    }

    toggleFilaColumna();
}

/*OBTENER MATRIZ + VALIDACIÓN*/
function obtenerMatriz() {
    const tam = Number(document.getElementById("tamano").value);

    clearInputErrors();

    const matriz = [];
    let valido = true;

    const prohibidos = /[a-df-zA-DF-Z,;:*\/\\]|e|E/;

    for (let f = 0; f < tam; f++) {
        const fila = [];
        for (let c = 0; c < tam; c++) {

            const input = document.getElementById(`c${f}_${c}`);
            let val = input.value.trim();

            if (val === "") { markInputError(input, "Campo vacío"); valido = false; continue; }
            if (prohibidos.test(val)) { markInputError(input, "Valor inválido"); valido = false; continue; }
            if (/(\+\+|\-\-|\+\-|\-\+)/.test(val)) { markInputError(input, "Signo duplicado"); valido = false; continue; }
            if (val.startsWith(".") || val.endsWith(".")) { markInputError(input, "Decimal inválido"); valido = false; continue; }

            fila.push(val);
        }
        matriz.push(fila);
    }

    return valido ? matriz : null;
}

/*RENDERIZADOR DE MATRICES VISUALES*/
function crearMatrizHTML(mat) {
    const cont = document.createElement("div");
    cont.classList.add("matrix-box");

    mat.forEach(fila => {
        const row = document.createElement("div");
        row.classList.add("matrix-row");

        fila.forEach(value => {
            const cell = document.createElement("div");
            cell.classList.add("matrix-cell");
            cell.innerText = value;
            row.appendChild(cell);
        });

        cont.appendChild(row);
    });

    return cont;
}

function mostrarPasosVisuales(header, pasos) {
    const panel = document.getElementById("pasos");
    panel.innerHTML = "";

    const h = document.createElement("div");
    h.classList.add("result-header");
    h.innerText = header;
    panel.appendChild(h);
    panel.appendChild(document.createElement("br"));

    pasos.forEach(p => {

        if (typeof p === "string") {
            const t = document.createElement("div");
            t.classList.add("paso-texto");
            t.innerText = p;
            panel.appendChild(t);
            return;
        }

        if (p.tipo === "texto") {
            const t = document.createElement("div");
            t.classList.add("paso-texto");
            t.innerText = p.valor;
            panel.appendChild(t);
            return;
        }

        if (p.tipo === "matriz") {
            const m = crearMatrizHTML(p.valor);
            panel.appendChild(m);
            return;
        }
    });
}

/*VARIABLES GLOBALES*/
let ultimosPasos = [];
let ultimoResultado = null;
let ultimoHeader = "";
let animando = false;

/*CALCULAR*/
async function calcular() {
    clearAlerts();
    document.getElementById("pasos").innerHTML = "";

    const tam = Number(document.getElementById("tamano").value);
    const metodo = document.getElementById("metodo").value;

    const matriz = obtenerMatriz();
    if (!matriz) { showError("Corrige los errores antes de continuar."); return; }

    let modo = null;
    let indice = null;

    if (tam === 4 && metodo === "cofactores") {
        modo = document.getElementById("modo").value;
        indice = Number(document.getElementById("indice").value);
        if (!modo || !indice) {
            showError("Debe elegir FILA/COLUMNA y un índice 1–4.");
            return;
        }
    }

    const datos = { matriz, metodo, modo, indice };

    try {
        const res = await fetch("/determinantes", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos)
        });

        const json = await res.json();

        if (json.error) {
            showError(json.error);
            return;
        }

        showOk("Cálculo realizado correctamente.");

        ultimosPasos = json.pasos || [];
        ultimoResultado = json.resultado;

        ultimoHeader = `Determinante = ${json.resultado}`;

        mostrarPasosVisuales(ultimoHeader, ultimosPasos);

    } catch (err) {
        console.error(err);
        showError("No se pudo conectar al servidor.");
    }
}

/*BOTONES*/
document.getElementById("btnCalcular").onclick = calcular;

document.getElementById("btnLimpiar").onclick = () => {
    document.querySelectorAll(".fila-matriz input").forEach(i => i.value = "");
    document.getElementById("pasos").innerText = "";
    ultimosPasos = [];
    ultimoHeader = "";
    ultimoResultado = null;
    clearInputErrors();
    clearAlerts();
};

document.getElementById("btnDescargar").onclick = () => {

    if (!ultimosPasos.length) {
        showError("Debe realizar un cálculo primero.");
        return;
    }

    let texto = ultimoHeader + "\n\n";

    ultimosPasos.forEach(p => {
        if (typeof p === "string") texto += p + "\n";
        else if (p.tipo === "texto") texto += p.valor + "\n";
        else if (p.tipo === "matriz") texto += JSON.stringify(p.valor) + "\n";
    });

    const blob = new Blob([texto], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "procedimiento.txt";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);

    showOk("Archivo descargado.");
};

document.getElementById("btnPasoAPaso").onclick = () => {

    if (!ultimosPasos.length) {
        showError("Primero realiza un cálculo.");
        return;
    }

    if (animando) return;
    animando = true;

    const panel = document.getElementById("pasos");
    panel.innerHTML = "";
    panel.appendChild(document.createTextNode(ultimoHeader));
    panel.appendChild(document.createElement("br"));
    panel.appendChild(document.createElement("br"));

    let i = 0;

    const id = setInterval(() => {
        if (i >= ultimosPasos.length) {
            clearInterval(id);
            animando = false;
            return;
        }

        const p = ultimosPasos[i];

        if (typeof p === "string") {
            const t = document.createElement("div");
            t.classList.add("paso-texto");
            t.innerText = p;
            panel.appendChild(t);

        } else if (p.tipo === "texto") {
            const t = document.createElement("div");
            t.classList.add("paso-texto");
            t.innerText = p.valor;
            panel.appendChild(t);

        } else if (p.tipo === "matriz") {
            panel.appendChild(crearMatrizHTML(p.valor));
        }

        panel.scrollTop = panel.scrollHeight;
        i++;

    }, 600);
};

document.getElementById("btnTema").onclick = () => {
    document.body.classList.toggle("dark");
    const btn = document.getElementById("btnTema");
    btn.innerText = document.body.classList.contains("dark")
        ? "Modo claro"
        : "Modo oscuro";
};

/*INICIALIZACIÓN*/
generarMatriz();
actualizarMetodos();

document.getElementById("tamano").onchange = () => {
    clearAlerts();
    actualizarMetodos();
    generarMatriz();
};

document.getElementById("metodo").onchange = () => {
    clearAlerts();
    generarMatriz();
};