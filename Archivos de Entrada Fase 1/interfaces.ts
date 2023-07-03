interface Actor {
    nombre: string;
    edad: number;
}

interface Pelicula {
    nombre: string;
    posicion: number;
}

interface Contrato {
    actor: Actor;
    pelicula: Pelicula;
}

let actores = ["Elizabeth Olsen", "Adam Sandler", "Christian Bale", "Jennifer Aniston"];
let peliculas = ["Avengers: Age of Ultron", "Mr. Deeds", "Batman: The Dark Knight", "Marley & Me"];

function contratar(actor: Actor, pelicula: Pelicula): Contrato {
    return {
        actor : actor,
        pelicula: pelicula
    };
}

function crearActor(nombre: string, edad: number): Actor {
    return {
        nombre : nombre,
        edad: edad
};
}

function crearPelicula(nombre: string, posicion: number): Pelicula {
    return {
        nombre : nombre,
        posicion: posicion
    };
}
function imprimir(contrato: Contrato) {
    console.log("Actor:", contrato.actor.nombre, "   Edad:", contrato.actor.edad);
    console.log("Pelicula:", contrato.pelicula.nombre, "   Genero:", contrato.pelicula.posicion);
}
function contratos() {
    let contrato: Contrato = {
        actor: { nombre: "", edad: 0 },
        pelicula: { nombre: "", posicion: 0 }
        };
    for (let i = 1; i < 3; i++) {
        
        if (i < 4) {
        let actor = crearActor(actores[i - 1], i + 38);
        let pelicula = crearPelicula(peliculas[i - 1], i);
        contrato = contratar(actor, pelicula);
        }
        imprimir(contrato);
    }
}

contratos();