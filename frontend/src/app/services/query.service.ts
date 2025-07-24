import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Caso, QuestionRequest } from '../models/question-request';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class QueryService {
  apiUrl: string = 'http://localhost:8000/api/v1';

  constructor(private readonly http: HttpClient) {}

  // Endpoint actual para preguntar
  preguntar(query: QuestionRequest): Observable<any> {
    query.filename = '';
    return this.http.post(`${this.apiUrl}/query`, query);
  }
  // Obtener casos
  obtenerCasos(estado: string): Observable<Caso[]> {
    return this.http.get<Caso[]>(`${this.apiUrl}/casos?estado=${estado}`);
  }
  // Crear un nuevo caso
  nuevoCaso(caso: Caso, partePolicial: File): Observable<any> {
    const formData = new FormData();
    formData.append('caso', JSON.stringify(caso));
    formData.append('partePolicial', partePolicial);

    return this.http.post(`${this.apiUrl}/casos`, formData);
  }
  // Utilizar caso existente para pedir veredicto
  usarCaso(casoId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/casos/${casoId}/usar`, {});
  }

  // Obtener casos Dashboard
  obtenerCasosDashboard(): Observable<Caso[]> {
    return this.http.get<Caso[]>(`${this.apiUrl}/casos/dashboard`);
  }
  // Obtener datos para gráficos del dashboard
  obtenerDashboardData(): Observable<any> {
    return this.http.get(`${this.apiUrl}/casos/dashboard-data`);
  }
 obtenerTodosLosCasos(): Observable<Caso[]> {
    return this.http.get<Caso[]>(`${this.apiUrl}/casos/todos`);
  }

}
