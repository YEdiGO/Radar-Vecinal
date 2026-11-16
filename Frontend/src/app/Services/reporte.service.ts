import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Reporte, TipoIncidente } from '../Interfaces/reporte';
import { API_URL } from './api.config';

@Injectable({ providedIn: 'root' })
export class ReporteService {
  private http = inject(HttpClient);

  listar(opciones: { soloMios?: boolean; idBarrio?: string; limite?: number } = {}) {
    let params = new HttpParams().set('limite', opciones.limite ?? 50);
    if (opciones.soloMios) params = params.set('solo_mios', true);
    if (opciones.idBarrio) params = params.set('id_barrio', opciones.idBarrio);
    return this.http.get<Reporte[]>(`${API_URL}/reportes`, { params });
  }

  crear(datos: { lat: number; lng: number; tipo: TipoIncidente; descripcion: string }) {
    return this.http.post<Reporte>(`${API_URL}/reportes`, datos);
  }

  votar(id: number, tipo: 'confirmo' | 'incorrecto') {
    return this.http.post<Reporte>(`${API_URL}/reportes/${id}/voto`, { tipo });
  }

  eliminar(id: number) {
    return this.http.delete<void>(`${API_URL}/reportes/${id}`);
  }

  moderar(id: number, estado: 'activo' | 'falso' | 'archivado') {
    return this.http.patch<Reporte>(`${API_URL}/reportes/${id}/estado`, { estado });
  }
}