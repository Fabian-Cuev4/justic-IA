import { QueryService } from './../services/query.service';
import { Component, OnInit } from '@angular/core';
import { Caso } from '../models/question-request';
import { marked } from 'marked';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-juez-ia',
  templateUrl: './juez-ia.component.html',
  styleUrl: './juez-ia.component.css',
  standalone: true,
  imports: [CommonModule,]

})
export class JuezIaComponent implements OnInit {
  casos: Caso[] = [];
  casoSeleccionado: Caso | null = null;
  veredicto: string | null = null;
  detalles: string | null = null;
  cargando: boolean = false;
  error: string = '';
  marked = marked;
  mostrarDetalles = false;
  veredictoFormateado = '';



  constructor(private readonly queryService: QueryService) { }

  ngOnInit() {
    this.obtenerCasos();
  }

  obtenerCasos() {
    this.cargando = true;
    this.queryService.obtenerCasos('pendiente').subscribe({
      next: (casos) => {
        this.casos = casos;
        this.cargando = false;
      },
      error: () => {
        this.error = 'No se pudieron cargar los casos.';
        this.cargando = false;
      }
    });
  }

  juzgarCaso(caso: Caso) {
    this.casoSeleccionado = caso;
    this.veredicto = null;
    this.detalles = null;
    this.cargando = true;
    this.queryService.usarCaso(caso.id!).subscribe({
      next: (respuesta: any) => {
        this.cargando = false;
        const texto = respuesta.answer as string;

        // Buscar la línea que contiene el veredicto directo
        const regex = /VEREDICTO DIRECTO:\s*(.*)/i;
        const match = texto.match(regex);

        // Si se encuentra, usarla como veredicto
        this.veredicto = match ? match[1].trim() : '⚠️ Veredicto no definido claramente.';
        this.veredictoFormateado = this.veredicto
          .replace(/Culpable/i, '<span class="text-red-600 font-bold">Culpable</span>')
          .replace(/Inocente/i, '<span class="text-green-600 font-bold">Inocente</span>');

        // Guardar todo el texto como detalle
        this.detalles = texto;

        this.mostrarDetalles = false;
        this.casoSeleccionado = caso;

        // ✅ Marcar el caso como sentenciado
        caso.estado = 'Sentenciado';

        // ✅ Eliminarlo de la lista visible
        this.casos = this.casos.filter(c => c.estado !== 'Sentenciado');
      },
      error: () => {
        this.cargando = false;
        this.error = 'No se pudo obtener el veredicto.';
      }
    });
  }
}
