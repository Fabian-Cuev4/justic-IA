
import { Component } from '@angular/core';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { QueryService } from '../services/query.service';
import { marked } from 'marked';
import { Caso } from '../models/question-request';
import { NgClass, NgFor, NgIf } from '@angular/common';
import { RouterModule } from '@angular/router';
@Component({
  selector: 'app-home',
  imports: [ReactiveFormsModule, NgFor, NgIf,NgClass, RouterModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
  
})
export class HomeComponent {
  queryForm: FormGroup = new FormGroup({
    question: new FormControl('', Validators.required),
    filename: new FormControl(''),
  });
  loading: boolean = false;
  loadingRes = false;
  response: any;
  marked = marked;
  casos: Caso[] = [];
  mostrarDashboard: boolean = false;

  // Para gráficos dinámicos
  totalCasos = 0;
  tiposDelito = [
    { tipo: 'Robo', color: '#2563EB', colorTailwind: 'bg-blue-700', value: 0 },
    { tipo: 'Fraude', color: '#F59E42', colorTailwind: 'bg-orange-400', value: 0 },
    { tipo: 'Otros', color: '#10B981', colorTailwind: 'bg-green-500', value: 0 },
  ];
  barrasFrecuentes: { tipo: string; color: string; porcentaje: number }[] = [];
  lineasMes: { tipo: string; color: string; data: number[] }[] = [];
  meses: string[] = [];

  constructor(private readonly queryService: QueryService) {}

  ngOnInit(){
    this.obtenerCasos();
  }

  obtenerCasos() {
    this.loading = true;
    this.queryService.obtenerCasosDashboard().subscribe({
      next: (casos) => {
        this.casos = casos;
        this.procesarGraficos();
      },
      complete: () => {
        this.loading = false;
      },
    });
  }

  procesarGraficos() {
    // Pie chart y total
    this.totalCasos = this.casos.length;
    const tipoMap: any = { Robo: 0, Fraude: 0, Otros: 0 };
    for (const caso of this.casos) {
      const tipo = caso.tipoDelito?.trim().toLowerCase();
      if (tipo === 'robo') tipoMap.Robo++;
      else if (tipo === 'fraude') tipoMap.Fraude++;
      else tipoMap.Otros++;

    }
    this.tiposDelito = this.tiposDelito.map(t => ({ ...t, value: tipoMap[t.tipo] }));

    // Barras más frecuentes (top 4)
    const counts: Record<string, number> = {};
    for (const caso of this.casos) {
      counts[caso.tipoDelito] = (counts[caso.tipoDelito] || 0) + 1;
    }
    const total = this.casos.length;
    this.barrasFrecuentes = Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 4)
      .map(([tipo, count], i) => {
        const color = [
          'bg-blue-600',
          'bg-green-500',
          'bg-orange-400',
          'bg-blue-300',
        ][i] || 'bg-gray-400';
        return {
          tipo,
          color,
          porcentaje: Math.round((count / total) * 100),
        };
      });

    // Gráfico de líneas: delitos por mes y tipo
    // 1. Obtener meses únicos ordenados
    const mesesSet = new Set<string>();
    for (const caso of this.casos) {
      if (caso.fecha) {
        const [y, m] = caso.fecha.split('-');
        mesesSet.add(`${y}-${m}`);
      }
    }
    this.meses = Array.from(mesesSet).sort();
    // 2. Para cada tipo, contar por mes
    const tipos = ['Robo', 'Fraude', 'Otros'];
    this.lineasMes = tipos.map((tipo, i) => {
      const color = [ '#2563EB', '#10B981', '#F59E42' ][i];
      const data = this.meses.map(mes =>
        this.casos.filter(c => {
          const tipoC = c.tipoDelito?.trim().toLowerCase();
          const mesC = c.fecha?.slice(0, 7);
          if (!mesC) return false;
          if (tipo === 'Otros') {
            return !['robo', 'fraude'].includes(tipoC) && mesC === mes;
          } else {
            return tipoC === tipo.toLowerCase() && mesC === mes;
          }
        }).length
      );
      console.log('▶️ Datos de línea generados:', data);

      return { tipo, color, data };
    });


    console.log('📊 tiposDelito:', this.tiposDelito);
    console.log('📈 lineasMes:', this.lineasMes);
    console.log('📅 meses:', this.meses);
    console.log('📦 totalCasos:', this.totalCasos);
    console.log('📄 casos[0]:', this.casos[0]);

  }

  // ...existing code...

  // Devuelve el path SVG para el segmento i del pie chart
  getPieArc(i: number): string {
    const total = this.tiposDelito.reduce((sum, t) => sum + t.value, 0);
    if (total === 0) return '';
    let startAngle = 0;
    for (let j = 0; j < i; j++) {
      startAngle += (this.tiposDelito[j].value / total) * 2 * Math.PI;
    }
    const angle = (this.tiposDelito[i].value / total) * 2 * Math.PI;
    const endAngle = startAngle + angle;
    const r = 50;
    const cx = 60, cy = 60;
    const x1 = cx + r * Math.cos(startAngle - Math.PI / 2);
    const y1 = cy + r * Math.sin(startAngle - Math.PI / 2);
    const x2 = cx + r * Math.cos(endAngle - Math.PI / 2);
    const y2 = cy + r * Math.sin(endAngle - Math.PI / 2);
    const largeArc = angle > Math.PI ? 1 : 0;
    return `M${cx},${cy} L${x1},${y1} A${r},${r} 0 ${largeArc},1 ${x2},${y2} Z`;
  }

  // Devuelve los puntos para el gráfico de líneas, escalando los valores
  getLinePoints(data: number[]): string {
  if (!data.length) return '';
  const minY = 10, maxY = 90;
  const maxVal = Math.max(...data, 1);
  if (data.length === 1) {
    const y = maxY - ((data[0] / maxVal) * (maxY - minY));
    return `30,${y} 290,${y}`;  // Línea horizontal fija
  }
  const stepX = 260 / (data.length - 1);
  return data.map((v, i) => {
    const x = 30 + i * stepX;
    const y = maxY - ((v / maxVal) * (maxY - minY));
    return `${x},${y}`;
  }).join(' ');
}


  send() {
    if (this.queryForm.invalid) {
      window.alert('Por favor, completa la pregunta.');
      return;
    }
    const query = this.queryForm.value;
    this.loadingRes = true;
    this.queryService.preguntar(query).subscribe({
      next: (response) => {
        this.response = response.answer;
      },
      error: (error) => {
        console.error('Error:', error);
      },
      complete: () => {
        this.loadingRes = false;
        this.queryForm.reset();
      },
    });
  }
}
