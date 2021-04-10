/* Основные настройки */
var 
    SCREEN_WIDTH = window.innerWidth, /* размеры области рисования */
    SCREEN_HEIGHT = window.innerHeight,
    ATOM_R = 0.2, /* радиус атома - колена ломаной */
    CYL_R = 0.1, /* радиус цилиндра - соединителя атомов */
    ATOM_DETALISATION = 10, /* количество полигонов на сфере */
    CYL_DETALISATION = 7, /* количество полигонов на цилиндре */
    MORPHING_DETALISATION = 8, /* количество шагов, за которое переходит текущий шаг морфинга в следующий */
    ROTATION_SENSE = Math.PI/20, /* Одно нажатие крутит на Math.PI / ROTATION_SENSETIVITY */
    EPS = 1e-5;
var /* различные уровни детализации сцены */
    GRAPHICS_DETALIZATION_LOW = 0,
    GRAPHICS_DETALIZATION_MEDIUM = 1,
    GRAPHICS_DETALIZATION_HIGH = 2,
    GRAPHICS_DETALIZATION_GREAT = 3;
    currentDetalization = 0;

var
    looping = false; 

/* Основные объекты */
var
    camera, scene, renderer, light, morph, 
    group, atoms, links; // группа объектов сцены, атомы и перемычки

var distD = 0, deltaY = 0, deltaX = 0; // отклонения на поворот объектов и удаление камеры
var permanentX = 0, permanentY = 0, permanentZ = 0.00; // постоянные составляющие вращения

/* Вспомогательные объекты */
var morphStep, morphDir, morphProgress = 0, isMorphing = false; /* morphDir = 1 - если на следующий морфинг, -1 - если на предыдущий */


function initGraphics() {
    var container = document.createElement('div');
    document.body.appendChild(container);

    /*var args = getUrlVars();
    if (args['webgl'] == 1) {
        if (!Detector.webgl) {
            Detector.addGetWebGLMessage();
        }
        renderer = new THREE.WebGLRenderer({antialias: true} );
    } else {
        renderer = new THREE.CanvasRenderer();
    }*/
    if (webgl) {
        if (!Detector.webgl) {
            Detector.addGetWebGLMessage();
        }
        renderer = new THREE.WebGLRenderer({antialias: true} );
        setDetalization(GRAPHICS_DETALIZATION_GREAT);
    } else {
        renderer = new THREE.CanvasRenderer();
        setDetalization(GRAPHICS_DETALIZATION_LOW);
    }
        
    renderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
    container.appendChild(renderer.domElement);
    /*
    // если нам не передали морфинга, тогда считаем, что его надо грузить get-ом с сервера
    if (morph == undefined) {
        if (args['req'] == undefined) {
            alert('No request specified');
            return false;
        }
        var s = httpGet('morph_requests/' + args['req'] + '.json');
        morph = eval(s);
        //console.debug(morph);
    }*/
}

function recreateScene() {
    var groupRotation = group.matrix.clone();
    var x = camera.position.x;
    initScene();
    group.matrix = (groupRotation);
    camera.position.x = x;
}

function initScene() {
    camera = new THREE.Camera(75, SCREEN_WIDTH / SCREEN_HEIGHT, 0, 1000);
    scene = new THREE.Scene();
    scene.addLight( new THREE.AmbientLight( 0x000020 ) );

    morphStep = 0;
    updateStats();
    var points = morph[0]; 

    var maxx = -10000, cx = 0, cy = 0, cz = 0;
    points.forEach(function (e) {
        cx += e[0];
        cy += e[1];
        cz += e[2];
        maxx = maxx < Math.abs(e[0]) ? Math.abs(e[0]) : maxx;
        maxx = maxx < Math.abs(e[1]) ? Math.abs(e[1]) : maxx;
        maxx = maxx < Math.abs(e[2]) ? Math.abs(e[2]) : maxx;
    });
    cx /= 1.0 * points.length;
    cy /= 1.0 * points.length;
    cz /= 1.0 * points.length;
    camera.position.x = 2 * Math.sqrt(3) * maxx;
    light = new THREE.PointLight(0xffffff, 1, 5 * Math.sqrt(3) * maxx);
    scene.addLight(light);
        
    group = new THREE.Object3D;
    atoms = [];
    links = [];
    
    for( var i = 0; i < points.length; i ++) {
        // текущие координаты атома, где структура сдвинута в центр масс
        var cur = new THREE.Vector3(points[i][0] - cx, points[i][1] - cy, points[i][2] - cz);
        // создаём новый атом
        var particle = co(new THREE.Sphere(ATOM_R, ATOM_DETALISATION, ATOM_DETALISATION));
        particle.position = new THREE.Vector3().copy(cur);
        // добавляем его куда следует
        atoms.push(particle);
        group.addChild(particle);
    }
    for( var i = 0; i < points.length - 1; i ++) {
        var cylinder = co(new THREE.Cylinder(CYL_DETALISATION, CYL_R, CYL_R, 1));
        group.addChild(cylinder);
        links.push(cylinder);
    }
    updateLinks();
    scene.addObject(group);

    document.addEventListener( 'mousedown', onDocumentMouseDown, false );
    document.addEventListener( 'mousemove', onDocumentMouseMove, false );
    document.addEventListener( 'mouseup', onDocumentMouseUp, false );
    document.addEventListener( 'touchstart', onDocumentTouchStart, false );
    document.addEventListener( 'touchmove', onDocumentTouchMove, false );
    document.addEventListener( 'touchend', onDocumentTouchEnd, false );
    document.onkeyup = function KeyCheck()  {
        switch(event.keyCode) {
            case 74: case 40:
                down(); break;
            case 72: case 37:
                left(); break;
            case 76: case 39:
                right(); break;
            case 75: case 38:
                up(); break;
            case 187: 
                zoomin(); break;
            case 189: case 188:
                zoomout(); break;
            case 78:
                nextMorph(); break;
            case 80:
                prevMorph(); break;
            case 32:
                stop();break;
            case 84:
                togglePlayback(); break;
            default:
                //console.debug(event.keyCode);
        }
    }
}

function init() {
    initGraphics();
    initScene();
}

function convexCombination(a, b, c) {
    return a * (1- c) + (c) * b;
}

function makeMorph(atoms, morphFrom, morphTo, morphProgress) {
    morphProtein(atoms, morph[morphFrom], morph[morphTo], morphProgress);
    updateLinks(atoms);
}

// на основании атомов создаёт между ними линки из цилиндров
function updateLinks() {
    // обновляем линки
    var cf = Math.sqrt(ATOM_R * ATOM_R - CYL_R * CYL_R);
    for(var i = 1; i < atoms.length; i = i + 1) {
        var cylinder = links[i - 1];
        cylinder.position.x = (atoms[i-1].position.x + atoms[i].position.x) / 2;
        cylinder.position.y = (atoms[i-1].position.y + atoms[i].position.y) / 2;
        cylinder.position.z = (atoms[i-1].position.z + atoms[i].position.z) / 2;
        cylinder.lookAt(atoms[i].position);
        var tmp = atoms[i - 1].position.distanceTo(atoms[i].position);
        cylinder.scale.z = tmp - 2 * cf;
        
        // супер условие на цвет!
//KV begin
//        var koeff = Math.abs(3.8 - tmp); 
//        if (koeff <= 0.1) koeff = 0.0; else koeff *= 5.0;
//        if (koeff > 1.0) koeff = 1.0;
//        cylinder.materials[0].color.g = 1 - koeff;
//        cylinder.materials[0].color.b = 1 - koeff;
        cylinder.materials[0].color.g = 1;
        cylinder.materials[0].color.b = 1;
//KV end
    }
}

/*
    Изменяет массив атомов, морфируя два состояния между собой
*/
function morphProtein(atoms, cur, next, koef) {

    //if (Math.abs(koef - 1) < EPS) return false;

    var cx = 0, cy = 0, cz = 0;
    for(var i = 0; i < cur.length; i ++) {
        cx += convexCombination(cur[i][0], next[i][0], koef);
        cy += convexCombination(cur[i][1], next[i][1], koef);
        cz += convexCombination(cur[i][2], next[i][2], koef);
    };
    cx /= 1.0 * next.length;
    cy /= 1.0 * next.length;
    cz /= 1.0 * next.length;
    // обновляем атомы
    for(var i = 0; i < atoms.length; i = i + 1) {
        atoms[i].position.x = convexCombination(cur[i][0], next[i][0], koef) - cx;
        atoms[i].position.y = convexCombination(cur[i][1], next[i][1], koef) - cy;
        atoms[i].position.z = convexCombination(cur[i][2], next[i][2], koef) - cz;
    }
}

function nextMorph() {
    if (isMorphing) return;
    if (morphStep + 1 >= morph.length) return;
    morphDir = 1;
    morphProgress = 0;
    isMorphing = true;
}

function prevMorph() {
    if (isMorphing) return;
    if (morphStep - 1 < 0) return;
    morphDir = - 1;
    morphProgress = 0;
    isMorphing = true;
}
function externalRotate(obj, deltaY, deltaX) {
    var mx = obj.matrix;
    var r1 = new THREE.Matrix4();
    r1.setRotationY(deltaY + permanentY);
    var r2 = new THREE.Matrix4();
    r2.setRotationZ(deltaX + permanentZ);
    var r3 = new THREE.Matrix4();
    r3.setRotationX(permanentX);

    r1.multiplySelf(r2).multiplySelf(mx);
    obj.rotation.setRotationFromMatrix(r1);
}

function render() {
    light.position.x = camera.position.x;

    if (Math.abs(deltaY) > EPS || Math.abs(deltaX) > EPS) {
        externalRotate(group, 0.05 * deltaY, 0.05 * deltaX);
        deltaY *= 0.95;
        deltaX *= 0.95;
    } else {
        deltaY = 0;
        deltaX = 0;
        externalRotate(group, 0, 0);
    }
    if (Math.abs(distD) > EPS) {
        camera.position.x += 0.05 *distD;
        distD *= 0.95;
    }
    if (isMorphing) {
        if (morphProgress == MORPHING_DETALISATION) {
            morphStep += morphDir;
            morphProgress = 0;
            if (looping) {
                if (morphStep == morph.length - 1 || morphStep == 0) morphDir = -morphDir;
            } else {
                isMorphing = false;
                updateStats();
            }
        } else {
            morphProgress += 1;
            makeMorph(atoms, morphStep, morphStep + morphDir, morphProgress/MORPHING_DETALISATION);
        }
    }
    
    renderer.render(scene, camera);
}

function animate() {
    requestAnimationFrame(animate);
    render();
}

function co(geometry) {
    var material = new THREE.MeshLambertMaterial( { color: 0xffffff, shading: THREE.FlatShading } );
    var m = new THREE.Mesh(geometry, material);
    m.overdraw = true;
    return m;
}

function zoomin() {
    distD = -camera.position.x / 2;
}

function zoomout() {
    distD = camera.position.x / 2;
}

function left() {
    deltaY -= ROTATION_SENSE;
}

function right() {
    deltaY += ROTATION_SENSE;
}
function up() {
    deltaX += ROTATION_SENSE;
}
function down() {
    deltaX -= ROTATION_SENSE;
}

function stop() {
    deltaX = 0;
    deltaY = 0;
    distD = 0;
}
var mouseX, mouseY, mouseDrag;
function onMouseDown(x, y) {
    mouseX = x;
    mouseY = y;
    mouseDrag = true;
}

function onMouseMove(x, y) {
    if (!mouseDrag) return;
    var dx = x - mouseX;
    var dy = y - mouseY;
    deltaX = -dy/20;
    deltaY = dx/20;
    mouseX = x;
    mouseY = y;
}

function onMouseUp(){
    mouseDrag = false;
}
                                                                                                                     
function onDocumentMouseDown(event) {
    onMouseDown(event.clientX, event.clientY);
}

function onDocumentMouseMove(event) {
    onMouseMove(event.clientX, event.clientY);
}

function onDocumentMouseUp(event) {
    onMouseUp(event.clientX, event.clientY);
}


function onDocumentTouchStart( event ) {
    if ( event.touches.length == 1 ) {
        event.preventDefault();
        onMouseDown(event.touches[0].pageX, event.touches[0].pageY);
    }
}
function onDocumentTouchMove( event ) {
    if ( event.touches.length == 1 ) {
        event.preventDefault();
        onMouseMove(event.touches[0].pageX, event.touches[0].pageY);
    }
}

function onDocumentTouchEnd( event ) {
    if ( event.touches.length == 1 ) {
        event.preventDefault();
        onMouseUp(event.touches[0].pageX, event.touches[0].pageY);
    }
}

// Возвращает аргументы ввиде массива
function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

// Синхронно посылает get запрос по адресу, результат - строка
function httpGet(theUrl) {
    var xmlHttp = null;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function getDetalization() {
    return currentDetalization;
}

function setDetalization(kind) {
    currentDetalization = kind;
    switch(kind) {
        case GRAPHICS_DETALIZATION_LOW:
            ATOM_DETALISATION = 2;
            CYL_DETALISATION = 3;
            break;
        case GRAPHICS_DETALIZATION_MEDIUM:
            ATOM_DETALISATION = 6;
            CYL_DETALISATION = 4;
            break;
        case GRAPHICS_DETALIZATION_HIGH:
            ATOM_DETALISATION = 10;
            CYL_DETALISATION = 7;
            break;
        case GRAPHICS_DETALIZATION_GREAT:
            ATOM_DETALISATION = 20;
            CYL_DETALISATION = 14;
            break;
    }
    if (scene != undefined) recreateScene();
}

function togglePlayback() {
    console.debug("done");
    looping = !looping;
    updateStats();
    if (!looping) return;
    isMorphing = true;
    if (morphStep == morph.length - 1) {
        morphDir = -1;
    } else {
        morphDir = 1;
    }
}

function updateStats() {
    var text = "Playback";
    if (!looping) {
        if (morphStep == 0) {
            text = "initial conformation";
        } else if (morphStep + 1 == morph.length) {
            text = "final conformation";
        } else {
            text = "intermediate: " + (morphStep) + "/" + (morph.length - 2);
        }
    }
    document.getElementById("morph-step").innerHTML = text;
}

//-----------------------------------------------------
//-----------------------------------------------------
//-----------------------------------------------------
//-----------------------------------------------------


// ТОЧКА ВХОДА
$(document).ready(function() {
/* Инициализация морфа */
    morph = eval($("#morphing").html());
    webgl = eval($("#webgl").html());

    init();
    animate();
});
