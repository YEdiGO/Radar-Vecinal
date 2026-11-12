import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { Barrio, PuntoCaliente, ZonaResumen } from '../Interfaces/zona';
import { API_URL } from './api.config';

@Injectable({ providedIn: 'root' })
export class ZonaService {
  private http = inject(HttpClient);

  /** Catálogo de barrios (público), disponible como signal. */
  readonly barrios = toSignal(this.http.get<Barrio[]>(`${API_URL}/barrios`), { initialValue: [] });

  zonas(tipo: string, dias: number) {
    let params = new HttpParams().set('dias', dias);
    if (tipo) params = params.set('tipo', tipo);
    return this.http.get<ZonaResumen[]>(`${API_URL}/zonas`, { params });
  }

  puntos(dias: number) {
    return this.http.get<PuntoCaliente[]>(`${API_URL}/zonas/puntos-calientes`, {
      params: { dias },
    });
  }
}