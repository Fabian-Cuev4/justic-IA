import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SafeUrlPipe } from '../pipes/safe-url.pipe';


@Component({
  standalone: true,
  selector: 'app-base-legal',
  imports: [CommonModule, FormsModule, SafeUrlPipe],
  templateUrl: './base-legal.component.html',
  styleUrls: ['./base-legal.component.css']
})

export class BaseLegalComponent {

  documentos = [
  { nombre: 'Código Orgánico Integral Penal', clave: 'coip_actualizado' },
  { nombre: 'Ley de armas', clave: 'ley_de_armas' },
  { nombre: 'Ley de integridad', clave: 'ley_integridad' },
  { nombre: 'Lista de cárceles', clave: 'carcel' }
];

pdfUrl: { [key: string]: string } = {
  coip_actualizado: '/coip_actualizado.pdf',
  ley_de_armas: '/ley_de_armas.pdf',
  ley_integridad: '/ley_integridad.pdf',
  carcel: '/carceles.pdf'
};

seleccionLey: string = 'coip_actualizado'}