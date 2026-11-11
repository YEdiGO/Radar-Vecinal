import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from './auth.service';

export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  return auth.usuario() ? true : inject(Router).createUrlTree(['/login']);
};

export const invitadoGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  return auth.usuario() ? inject(Router).createUrlTree([auth.inicio()]) : true;
};

export const vecinoGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  if (!auth.usuario()) return inject(Router).createUrlTree(['/login']);
  return auth.esMunicipalidad() ? inject(Router).createUrlTree(['/municipalidad']) : true;
};

export const municipalidadGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  if (!auth.usuario()) return inject(Router).createUrlTree(['/login']);
  return auth.esMunicipalidad() ? true : inject(Router).createUrlTree(['/']);
};