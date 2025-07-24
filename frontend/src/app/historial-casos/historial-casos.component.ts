import { Component, OnInit } from '@angular/core';
import { QueryService } from '../services/query.service';
import { Caso } from '../models/question-request';
import { DatePipe, NgClass, NgFor, NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-historial-casos',
  imports: [NgClass,FormsModule, NgFor, NgIf, DatePipe],
  templateUrl: './historial-casos.component.html',
  styleUrl: './historial-casos.component.css',
})
export class HistorialCasosComponent implements OnInit {
  casos: Caso[] = [];
  casosFiltrados: Caso[] = [];
  tipoDelito: string = '';
  estado: string = '';
  busqueda: string = '';
  cargando: boolean = false;
  error: string = '';

  tiposDelito = [
    'Amenazas',
    'Robo',
    'Fraude',
    'Lesiones',
    // Agrega más si es necesario
  ];
  estados = [
    'Pendiente',
    'Sentenciado'
  ];

  constructor(private readonly queryService: QueryService) {}

  ngOnInit() {
    this.obtenerCasos();
  }

  obtenerCasos() {
    this.cargando = true;
    // Si quieres todos los casos, puedes modificar el servicio para no filtrar por estado
    this.queryService.obtenerTodosLosCasos().subscribe({
      next: (casos) => {
        this.casos = casos;
        this.casosFiltrados = casos;
        this.cargando = false;
      },
      error: () => {
        this.error = 'No se pudieron cargar los casos.';
        this.cargando = false;
      }
    });
  }

  filtrar() {
    this.casosFiltrados = this.casos.filter(caso => {
      const coincideDelito = this.tipoDelito
        ? caso.tipoDelito?.toLowerCase() === this.tipoDelito.toLowerCase()
        : true;
      const coincideEstado = this.estado
        ? caso.estado?.toLowerCase() === this.estado.toLowerCase()
        : true;
      const coincideBusqueda = this.busqueda
        ? (caso.nombre?.toLowerCase().includes(this.busqueda.toLowerCase()) ||
           caso.id?.toString().includes(this.busqueda))
        : true;
      return coincideDelito && coincideEstado && coincideBusqueda;
    });
  }

  onBuscar(event: Event) {
    event.preventDefault();
    this.filtrar();
  }

  onTipoDelitoChange(event: Event) {
    const select = event.target as HTMLSelectElement;
    this.tipoDelito = select.value !== 'Tipo de delito' ? select.value : '';
    this.filtrar();
  }

  onEstadoChange(event: Event) {
    const select = event.target as HTMLSelectElement;
    this.estado = select.value !== 'Estado' ? select.value : '';
    this.filtrar();
  }

  onBusquedaChange(event: Event) {
    const input = event.target as HTMLInputElement;
    this.busqueda = input.value;
    // No filtra en tiempo real, solo al buscar
  }
}
