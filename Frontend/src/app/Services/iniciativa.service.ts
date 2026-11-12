import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { EstadoIniciativa, Iniciativa } from '../Interfaces/iniciativa';
import { API_URL } from './api.config';

@Injectable({ providedIn: 'root' })
export class IniciativaService {
  private http = inject(HttpClient);

  listar(idBarrio = '') {
    let params = new HttpParams();
    if (idBarrio) params = params.set('id_barrio', idBarrio);
    return this.http.get<Iniciativa[]>(`${API_URL}/iniciativas`, { params });
  }

  crear(datos: { id_barrio: string; titulo: string; descripcion: string; meta: string }) {
    return this.http.post<Iniciativa>(`${API_URL}/iniciativas`, datos);
  }

  participar(id: number) {
    return this.http.post<Iniciativa>(`${API_URL}/iniciativas/${id}/participar`, {});
  }

  cambiarEstado(id: number, estado: EstadoIniciativa) {
    return this.http.patch<Iniciativa>(`${API_URL}/iniciativas/${id}/estado`, { estado });
  }
}