// ==========================
function generarMatriz() {
    const t = parseInt(document.getElementById("tamano").value);
    const cont = document.getElementById("matrizInputs");

    cont.innerHTML = "";

    for (let i = 0; i < t; i++) {
        const fila = document.createElement("div");
        fila.classList.add("fila-matriz");

        for (let j = 0; j < t; j++) {
            const input = document.createElement("input");
            input.type = "text";
            input.id = `c${i}_${j}`;
            fila.appendChild(input);
        }
        cont.appendChild(fila);
    }

    // Mostrar fila/columna si es 4x4
    document.getElementById("filaColumnaRow").style.display = t === 4 ? "flex" : "none";
}

generarMatriz();
document.getElementById("tamano").addEventListener("change", generarMatriz);


// ==========================
function alertaError(msg) {
    const a = document.getElementById("alertaError");
    a.innerText = msg;
    a.style.display = "block";
    document.getElementById("alertaOk").style.display = "none";
}

function alertaOk(msg) {
    const a = document.getElementById("alertaOk");
    a.innerText = msg;
    a.style.display = "block";
    document.getElementById("alertaError").style.display = "none";
}

function limpiarAlertas() {
    document.getElementById("alertaError").style.display = "none";
    document.getElementById("alertaOk").style.display = "none";
}


// ==========================
function marcarError(input, msg) {
    input.classList.add("input-error");
    const m = document.createElement("div");
    m.classList.add("error-msg");
    m.innerText = msg;
    if (input.nextSibling) {
        input.parentNode.insertBefore(m, input.nextSibling);
    } else {
        input.parentNode.appendChild(m);
    }
}

function obtenerMatriz() {
    const t = parseInt(document.getElementById("tamano").value);
    const matriz = [];
    let valido = true;

    document.querySelectorAll(".error-msg").forEach(e => e.remove());
    document.querySelectorAll(".fila-matriz input").forEach(i => i.classList.remove("input-error"));

    const prohibidos = /[a-df-zA-DF-Z,;:*/\\]|e|E/;

    for (let i = 0; i < t; i++) {
        const fila = [];
        for (let j = 0; j < t; j++) {
            const input = document.getElementById(`c${i}_${j}`);
            let val = input.value.trim();

            if (val === "") {
                valido = false;
                marcarError(input, `El campo (${i+1},${j+1}) está vacío`);
                continue;
            }

            if (prohibidos.test(val)) {
                valido = false;
                marcarError(input, `Valor inválido`);
                continue;
            }

            if (val.includes("++") || val.includes("--") || val.includes("+-") || val.includes("-+")) {
                valido = false;
                marcarError(input, `Signo duplicado`);
                continue;
            }

            if (val.startsWith(".") || val.endsWith(".")) {
                valido = false;
                marcarError(input, `Formato decimal inválido`);
                continue;
            }

            fila.push(val);
        }
        matriz.push(fila);
    }

    if (!valido) return null;
    return matriz;
}


// ==========================
let ultimosPasos = [];
let ultimoResultado = null;
let animando = false;


// ==========================
document.getElementById("btnCalcular").addEventListener("click", async () => {
    limpiarAlertas();

    const matriz = obtenerMatriz();
    if (!matriz) {
        alertaError("Corrige los errores en la matriz antes de calcular.");
        return;
    }

    const tam = parseInt(document.getElementById("tamano").value);
    const metodo = document.getElementById("metodo").value;

    if (tam === 4 && metodo === "sarrus") {
        alertaError("El método de Sarrus solo aplica para matrices 3×3. Usa cofactores en 4×4.");
        return;
    }

    let modo = null;
    let indice = null;

    if (tam === 4) {
        modo = document.getElementById("modo").value;
        indice = parseInt(document.getElementById("indice").value);
    }

    const datos = {
        matriz: matriz,
        metodo: metodo,
        modo: modo,
        indice: indice
    };

    try {
        const res = await fetch("/determinantes", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos)
        });

        const json = await res.json();

        if (json.error) {
            alertaError(json.error);
            document.getElementById("pasos").innerText = "";
            ultimosPasos = [];
            ultimoResultado = null;
            return;
        }

        alertaOk("Determinante calculado correctamente.");

        ultimoResultado = json.resultado;
        ultimosPasos = json.pasos || [];

        const panel = document.getElementById("pasos");
        panel.innerText = `Determinante = ${json.resultado}\n\n` + ultimosPasos.join("\n");

    } catch (err) {
        console.error(err);
        alertaError("No se pudo conectar con el servidor.");
    }
});


// ==========================
document.getElementById("btnLimpiar").addEventListener("click", () => {
    document.querySelectorAll(".fila-matriz input").forEach(i => i.value = "");
    document.getElementById("pasos").innerText = "";
    document.querySelectorAll(".error-msg").forEach(e => e.remove());
    document.querySelectorAll(".fila-matriz input").forEach(i => i.classList.remove("input-error"));
    ultimosPasos = [];
    ultimoResultado = null;
    limpiarAlertas();
});


// ==========================
document.getElementById("btnDescargar").addEventListener("click", () => {
    if (ultimosPasos.length === 0) {
        alertaError("Primero calcule un determinante para poder descargar los pasos.");
        return;
    }

    let contenido = `Determinante = ${ultimoResultado}\n\n`;
    contenido += ultimosPasos.join("\n");

    const blob = new Blob([contenido], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "determinante_pasos.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    alertaOk("Archivo de pasos descargado correctamente.");
});

// ==========================
document.getElementById("btnPasoAPaso").addEventListener("click", () => {
    if (ultimosPasos.length === 0) {
        alertaError("Calcula primero un determinante para ver los pasos.");
        return;
    }

    if (animando) return;
    animando = true;

    const panel = document.getElementById("pasos");
    panel.innerText = `Determinante = ${ultimoResultado}\n\n`;

    let idx = 0;

    const id = setInterval(() => {
        if (idx >= ultimosPasos.length) {
            clearInterval(id);
            animando = false;
            return;
        }
        panel.innerText += ultimosPasos[idx] + "\n";
        panel.scrollTop = panel.scrollHeight;
        idx++;
    }, 600);
});

// ==========================
document.getElementById("btnTema").addEventListener("click", () => {
    const body = document.body;
    body.classList.toggle("dark");

    const btn = document.getElementById("btnTema");
    if (body.classList.contains("dark")) {
        btn.innerText = "Modo claro";
    } else {
        btn.innerText = "Modo oscuro";
    }
});
