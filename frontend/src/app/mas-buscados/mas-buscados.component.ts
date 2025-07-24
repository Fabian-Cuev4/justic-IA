import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SafeUrlPipe } from '../pipes/safe-url.pipe';

@Component({
  selector: 'app-mas-buscados',
  standalone: true,
  imports: [CommonModule, FormsModule, SafeUrlPipe],
  templateUrl: './mas-buscados.component.html',
  styleUrls: ['./mas-buscados.component.css']
})
export class MasBuscadosComponent {
  // Lista de categorías
  categorias = [
    { clave: 'corrupcion', nombre: 'Delitos de corrupción' },
    { clave: 'genero', nombre: 'Violencia de género' },
    { clave: 'publico', nombre: 'Delitos de ejercicio público' }
  ];

  // Selección activa
  delitoSeleccionado: string = 'corrupcion';

  // PDF por categoría
  pdfUrl: { [key: string]: string } = {
    corrupcion: '/corrupcion.pdf',
    genero: '/genero.pdf',
    publico: '/publico.pdf'
  };
}