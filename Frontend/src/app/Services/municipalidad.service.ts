import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { AccionMunicipal, EstadoAccion, Estadisticas } from '../Interfaces/municipalidad';
import { ZonaResumen } from '../Interfaces/zona';
import { API_URL } from './api.config';

@Injectable({ providedIn: 'root' })
export class MunicipalidadService {
  private http = inject(HttpClient);

  criticos() {
    return this.http.get<ZonaResumen[]>(`${API_URL}/municipalidad/criticos`);
  }

  estadisticas() {
    return this.http.get<Estadisticas>(`${API_URL}/municipalidad/estadisticas`);
  }

  acciones(opciones: { idBarrio?: string; soloMias?: boolean } = {}) {
    let params = new HttpParams();
    if (opciones.idBarrio) params = params.set('id_barrio', opciones.idBarrio);
    if (opciones.soloMias) params = params.set('solo_mias', true);
    return this.http.get<AccionMunicipal[]>(`${API_URL}/acciones`, { params });
  }

  crearAccion(datos: {
    id_barrio: string; tipo: string; titulo: string;
    descripcion: string; fecha: string; estado: string;
  }) {
    return this.http.post<AccionMunicipal>(`${API_URL}/acciones`, datos);
  }

  cambiarEstadoAccion(id: number, estado: EstadoAccion) {
    return this.http.patch<AccionMunicipal>(`${API_URL}/acciones/${id}/estado`, { estado });
  }
}