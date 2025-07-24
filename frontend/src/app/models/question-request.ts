export interface QuestionRequest {
    question: string;
    filename: string;
}

export interface Caso {
    tipoDelito:string
    nombre:string
    fecha?:string
    estado?:string
    id?:number
    veredicto?:string
}
