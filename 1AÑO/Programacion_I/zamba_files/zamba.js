var VERSION_CODIGO = 1.0;
var actividad = ""

/// Tipos de rutinas
const RUTINAS = {
    FUNCION: 'return',
    PROCEDIMIENTO: 'noreturn'
};
delete Blockly.Blocks.math_change;

var color_texto = "#000000";

var blocklyArea = document.getElementById('blocklyArea');
var blocklyDiv = document.getElementById('blocklyDiv');
var onresize = function(e) {
    // Compute the absolute coordinates and dimensions of blocklyArea.
    var element = blocklyArea;
    var x = 0;
    var y = 0;
    do {
      x += element.offsetLeft;
      y += element.offsetTop;
      element = element.offsetParent;
    } while (element);
    // Position blocklyDiv over blocklyArea.
    blocklyDiv.style.left = x + 'px';
    blocklyDiv.style.top = y + 'px';
    blocklyDiv.style.width = blocklyArea.offsetWidth + 'px';
    blocklyDiv.style.height = blocklyArea.offsetHeight + 'px';
    Blockly.svgResize(workspace);
};

var workspace = Blockly.inject('blocklyDiv',
    {
        toolbox : document.getElementById('toolbox'),
        collapse : true, 
    	comments : true,         
        trashcan : true,        
        sounds : true,
        scrollbars : true,
        zoom : {
            controls: true,
            wheel: true,
            startScale: 1,
            maxScale: 3,
            minScale: 0.3,
            scaleSpeed: 1.2
        }
    });

// Registra la función generadora de bloques para la categoría MIS_FUNCIONES
workspace.registerToolboxCategoryCallback('MIS_FUNCIONES', misFuncionesCallback);
// Registra la función generadora de bloques para la categoría MIS_PROCEDIMIENTOS
workspace.registerToolboxCategoryCallback('MIS_PROCEDIMIENTOS', misProcedimientosCallback);
// Deshabilita los bloques huérfanos
workspace.addChangeListener(Blockly.Events.disableOrphans);

// Exit is used to signal the end of a script.
Blockly.JavaScript.addReservedWords('exit');

window.addEventListener('resize', onresize, false);
onresize();
Blockly.svgResize(workspace);

agregarBloqueInicial(workspace);

function myUpdateFunction(event) {
    let code = Blockly.Python.workspaceToCode(workspace);
    
    document.getElementById('codigo_python').value = code;
    //document.getElementById('codigo_python').innerHTML = code;
    if (!(event instanceof Blockly.Events.Ui)) {
        // Something changed. Parser needs to be reloaded.
        resetInterpreter();
        generateCodeAndLoadIntoInterpreter();
    }
}

var outputArea = document.getElementById('salida');
var myInterpreter = null;
var highlightPause = false;
var runButton = document.getElementById('ejecutar');
var stopButton = document.getElementById('detener');
var latestCode = '';
var runner;
var modoEjecucion = document.getElementById('modoEjecucion');
function initApi(interpreter, globalObject) {

    Blockly.DOMParser = window.DOMParser;
    Blockly.Element = window.Element;
    Blockly.document = window.document;


    // Add an API function for the imprimir() block.
    let func_imprimir = function (valor) {
        return imprimir(valor);
    };
    interpreter.setProperty(globalObject, 'imprimir',
    interpreter.createNativeFunction(func_imprimir));

    // Add an API function for the obtenerEntrada() block.
    let func_obtenerEntrada = function (valor) {
        return obtenerEntrada(valor);
    };
    interpreter.setProperty(globalObject, 'obtenerEntrada',
    interpreter.createNativeFunction(func_obtenerEntrada));

    // Add an API function for the obtenerEntrada() block.
    let func_obtenerEntradaNumerica = function (valor) {
        return obtenerEntradaNumerica(valor);
    };
    interpreter.setProperty(globalObject, 'obtenerEntradaNumerica',
    interpreter.createNativeFunction(func_obtenerEntradaNumerica));

    // Add an API function for the longitudCadena() block.
    let func_longitudCadena = function (valor) {
        return longitudCadena(valor);
    };
    interpreter.setProperty(globalObject, 'longitudCadena',
    interpreter.createNativeFunction(func_longitudCadena));

    // Add an API function for the caracterCadena() block.
    let func_caracterCadena = function (cadena, posicion) {
        return caracterCadena(cadena, posicion);
    };
    interpreter.setProperty(globalObject, 'caracterCadena',
    interpreter.createNativeFunction(func_caracterCadena));

    // Add an API function for the cambiarColorTexto() block.
    let func_cambiarColorTexto = function (color) {
        return cambiarColorTexto(color);
    };
    interpreter.setProperty(globalObject, 'cambiarColorTexto',
    interpreter.createNativeFunction(func_cambiarColorTexto));


    // Add an API function for highlighting blocks.
    let func_highlightBlock = function (id) {
        return workspace.highlightBlock(id);
    };
    interpreter.setProperty(globalObject, 'highlightBlock',
        interpreter.createNativeFunction(func_highlightBlock));

}

function highlightBlock(id) {
    workspace.highlightBlock(id);
    highlightPause = true;
}


function resetStepUi(clearOutput) {
    workspace.highlightBlock(null);
    highlightPause = false;
    runButton.disabled = '';
    stopButton.disabled = 'disabled';
    if (clearOutput) {
        outputArea.innerHTML = '';
    }
}

function generateCodeAndLoadIntoInterpreter() {
    Blockly.JavaScript.STATEMENT_PREFIX = 'highlightBlock(%1);\n';
    Blockly.JavaScript.addReservedWords('highlightBlock');
    Blockly.JavaScript.addReservedWords('latestCode')
    window.LoopTrap = 1000;
    Blockly.JavaScript.INFINITE_LOOP_TRAP = 'if(--window.LoopTrap == 0) throw "Infinite loop.";\n';
    resetStepUi(true);
    return;
}

function resetInterpreter() {
    myInterpreter = null;
    if (runner) {
        clearTimeout(runner);
        runner = null;
    }
    return;
}

function ejecutar() {
    initVariables();
    latestCode = Blockly.JavaScript.workspaceToCode(workspace);
    if (!myInterpreter) {
        initVariables();
        resetStepUi(true);
        runButton.disabled = 'disabled';
        stopButton.disabled = '';
        myInterpreter = new Interpreter(latestCode, initApi);
        if (!modoEjecucion.checked)
            runStepByStep();
        else
            runFullSpeed();
    }
    return;
}

function detener() {
    if (myInterpreter) {
        resetInterpreter();
        resetStepUi(false);
    }
    return;
}

function runStepByStep() {
    if (myInterpreter) {
        if (myInterpreter.step()) {
            setTimeout(runStepByStep, 5);
        }
        else {
            resetInterpreter();
            resetStepUi(false);
        }
    }
    return;
}

function runFullSpeed() {
    if (myInterpreter) {
        let hayMasCodigo = myInterpreter.run();
        if (hayMasCodigo) {
            setTimeout(runFullSpeed, 10);
        } 
        else {
            resetInterpreter();
            resetStepUi(false);
        }
    }
    return;
}

// Load the interpreter now, and upon future changes.
generateCodeAndLoadIntoInterpreter();
workspace.addChangeListener(myUpdateFunction);


function initVariables() {
    color_texto = "#000000";
}

/**
 * @param valor es el valor a imprimir, siempre se convierte a string
*/
function imprimir(valor) {
    let texto = (valor != null) ? valor.toString() : '';
    outputArea.innerHTML = outputArea.innerHTML + "<span style='color:" + color_texto + "'>" + texto + "</span>" + "<br>";
    return;
}

/**
 * @param textoMensaje es el texto para el mensaje del input
 */
function obtenerEntrada(textoMensaje) {
    return prompt(textoMensaje);
}

/**
 * @param cadena es una cadena de texto
 */
function longitudCadena(cadena) {
    return (cadena != null) ? cadena.length : 0;
}

/**
 * @param cadena es una cadena de texto
 * @param posicion es un entero
 */
function caracterCadena(cadena, posicion) {
    return (cadena != null) ? cadena.charAt(posicion)  : '';
}

/**
 * @param color es una cadena de la forma #RRGGBB 
 */
function cambiarColorTexto(color) {
    color_texto = color;
    return;
}

/**
 * Función de gestión para la categoría "MIS_FUNCIONES" del Toolbox.
 * @param {!Blockly.Workspace} Espacio de trabajo de Blockly.
 * @return {!Array.<!Element>} Lista con bloques de tipo "llamada a función" (formato XML).
 */
function misFuncionesCallback(workspace) {
    return generarBloquesFuncionProcedimiento(workspace, RUTINAS.FUNCION);
}

/**
 * Función de gestión para la categoría "MIS_PROCEDIMIENTOS" del Toolbox.
 * @param {!Blockly.Workspace} Espacio de trabajo de Blockly.
 * @return {!Array.<!Element>} Lista con bloques de tipo "llamada a procedimiento" (formato XML).
 */
function misProcedimientosCallback(workspace) {
    return generarBloquesFuncionProcedimiento(workspace, RUTINAS.PROCEDIMIENTO);
}

/**
 * Genera, al vuelo, los bloques de llamada para cada función/procedimiento definido en el workspace.
 * @param {!Blockly.Workspace} Espacio de trabajo de Blockly.
 * @return {!Array.<!Element>} Lista con bloques de tipo "llamada a función/procedimiento" (formato XML).
 */
function generarBloquesFuncionProcedimiento(workspace, tipoRutina) {
    let xmlList = [];
    let procedureDefs = workspace.getBlocksByType('procedures_def' + tipoRutina, true);
    for (let procIdx in procedureDefs) {
        let blockText = '<block type="procedures_call' + tipoRutina + '">' +
                        '<field name="NAME">' + procedureDefs[procIdx].getFieldValue('NAME') + '</field>';

        if (procedureDefs[procIdx].arguments_.length > 0) {
            blockText += '<mutation>';
            for (let argIdx in procedureDefs[procIdx].arguments_) {
                blockText += '<arg name="' + procedureDefs[procIdx].arguments_[argIdx] + '"></arg>';
            }
            blockText += '</mutation>';
        }
        blockText += '</block>';
        let block = Blockly.Xml.textToDom(blockText);
        xmlList.push(block);
    }
    return xmlList;
}

document.getElementById('file-upload')
    .addEventListener('change', leerSolucionWeb, false);

function leerSolucionWeb(e) {
    var archivo = e.target.files[0];
    if (!archivo) {
        return;
    }
    var reader = new FileReader();
    return new Promise((resolve, reject) => {
        reader.onerror = err => reject(err);

        reader.onload = event => resolve(event.target.result);

        reader.readAsText(archivo);
    }).then(contenido => cargarPrograma(contenido));
}

function cargarPrograma(contenido) {
    let data = null;
    let solucion = null;

    try {
        data = JSON.parse(contenido);
        solucion = atob(data.solucion);
        let workspace = Blockly.getMainWorkspace();
        workspace.clear();
        Blockly.Xml.domToWorkspace(Blockly.Xml.textToDom(solucion), workspace);
    } catch (e) {
        console.error(e);
        alert("Lo siento, este archivo no tiene una solución ZAMBA.");
    }

    let errors = [];

    if (errors.length !== 0) {
        let e = errors.join('\n')
        console.error(e);
        alert(e);
    }
    return;
}

function grabarPrograma() {
    if (nombreArchivo = prompt("Nombre del archivo", "programa.zmb")){
        let contenido = {
            version: VERSION_CODIGO,
            actividad: actividad,
            solucion: btoa(Blockly.Xml.domToPrettyText(Blockly.Xml.workspaceToDom(Blockly.getMainWorkspace())))
        };

        let a = document.createElement("a");
        a.download = nombreArchivo;
        a.href = URL.createObjectURL(new Blob([JSON.stringify(contenido)], {type: 'application/octet-stream'}));
        a.type = 'application/octet-stream';
        a.click();
    }
    return;
}

function copiarCodigo() {
    let textarea = document.getElementById("codigo_python");
    textarea.select();
    document.execCommand("copy");
    document.getSelection().removeAllRanges();
    return;
}

function conmutarTab(evt, nombreTab) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for(i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for(i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(nombreTab).style.display = "block";
    evt.currentTarget.className += " active";
    return;
}

function nuevoPrograma() {
    let workspace = Blockly.getMainWorkspace();
    if (confirm("¿Comenzar un programa nuevo?")){    
        workspace.clear();
        agregarBloqueInicial(workspace);
    }
    return;
}

function agregarBloqueInicial(workspace) {
    var xml = '<xml>' +
              '<block type="inicio" deletable="false" movable="false"></block>' +
              '</xml>';
    Blockly.Xml.domToWorkspace(Blockly.Xml.textToDom(xml), workspace);
    return;
}