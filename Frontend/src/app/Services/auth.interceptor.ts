import { isPlatformBrowser } from '@angular/common';
import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { PLATFORM_ID, inject } from '@angular/core';
import { API_URL } from './api.config';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  if (!isPlatformBrowser(inject(PLATFORM_ID))) return next(req);
  const token = localStorage.getItem('rv_token');
  if (!token || req.url.startsWith(`${API_URL}/auth/`)) return next(req);
  return next(req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }));
};

export function mensajeError(error: unknown): string {
  if (error instanceof HttpErrorResponse) {
    const detail = error.error?.detail;
    if (typeof detail === 'string') return detail;
    if (Array.isArray(detail)) {
      return detail
        .map((d: { msg?: string }) => d?.msg ?? String(d))
        .join(' ');
    }
    if (error.status === 0) return 'No se pudo conectar con el servidor.';
    return error.message || `Error ${error.status}.`;
  }
  return error instanceof Error ? error.message : 'Ocurrió un error inesperado.';
}
