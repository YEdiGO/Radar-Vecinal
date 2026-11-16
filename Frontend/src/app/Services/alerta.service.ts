import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Alerta } from '../Interfaces/alerta';
import { API_URL } from './api.config';

@Injectable({ providedIn: 'root' })
export class AlertaService {
  private http = inject(HttpClient);

  activas() {
    return this.http.get<Alerta[]>(`${API_URL}/alertas/activas`);
  }

  crear(datos: { id_barrio: string; motivo: string; ubicacion: string }) {
    return this.http.post<Alerta>(`${API_URL}/alertas`, datos);
  }
}