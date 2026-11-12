import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Injectable, PLATFORM_ID, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { tap } from 'rxjs';
import { TokenRespuesta, Usuario } from '../Interfaces/usuario';
import { API_URL } from './api.config';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private esNavegador = isPlatformBrowser(inject(PLATFORM_ID));

  private _usuario = signal<Usuario | null>(null);
  readonly usuario = this._usuario.asReadonly();
  readonly esMunicipalidad = computed(() => this._usuario()?.rol === 'municipalidad');

  constructor() {
    if (this.esNavegador) {
      const raw = localStorage.getItem('rv_usuario');
      if (raw) this._usuario.set(JSON.parse(raw));
    }
  }

  get token(): string | null {
    return this.esNavegador ? localStorage.getItem('rv_token') : null;
  }

  login(datos: { correo: string; clave: string }) {
    return this.http.post<TokenRespuesta>(`${API_URL}/auth/login`, datos).pipe(tap((r) => this.guardar(r)));
  }

  registro(datos: { nombre: string; correo: string; clave: string; id_barrio: string }) {
    return this.http.post<TokenRespuesta>(`${API_URL}/auth/registro`, datos).pipe(tap((r) => this.guardar(r)));
  }

  salir() {
    if (this.esNavegador) {
      localStorage.removeItem('rv_token');
      localStorage.removeItem('rv_usuario');
    }
    this._usuario.set(null);
    this.router.navigate(['/login']);
  }

  inicio(): string {
    return this.esMunicipalidad() ? '/municipalidad' : '/';
  }

  private guardar(r: TokenRespuesta) {
    if (this.esNavegador) {
      localStorage.setItem('rv_token', r.access_token);
      localStorage.setItem('rv_usuario', JSON.stringify(r.usuario));
    }
    this._usuario.set(r.usuario);
  }
}