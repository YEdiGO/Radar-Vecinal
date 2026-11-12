import { Routes } from '@angular/router';
import { authGuard, invitadoGuard, municipalidadGuard, vecinoGuard } from './Services/auth.guard';

export const routes: Routes = [
  {
    path: 'login', canActivate: [invitadoGuard],
    loadComponent: () => import('./Components/login/login').then((m) => m.Login),
  },
  {
    path: 'registro', canActivate: [invitadoGuard],
    loadComponent: () => import('./Components/registro/registro').then((m) => m.Registro),
  },
  {
    path: '', pathMatch: 'full', canActivate: [authGuard],
    loadComponent: () => import('./Components/mapa/mapa').then((m) => m.Mapa),
  },
  {
    path: 'reportes', canActivate: [vecinoGuard],
    loadComponent: () => import('./Components/reportes/reportes').then((m) => m.Reportes),
  },
  {
    path: 'reportes/nuevo', canActivate: [vecinoGuard],
    loadComponent: () => import('./Components/reporte-form/reporte-form').then((m) => m.ReporteForm),
  },
  {
    path: 'iniciativas', canActivate: [authGuard],
    loadComponent: () => import('./Components/iniciativas/iniciativas').then((m) => m.Iniciativas),
  },
  {
    path: 'iniciativas/nueva', canActivate: [vecinoGuard],
    loadComponent: () => import('./Components/iniciativa-form/iniciativa-form').then((m) => m.IniciativaForm),
  },
  {
    path: 'mi-barrio', canActivate: [vecinoGuard],
    loadComponent: () => import('./Components/mi-barrio/mi-barrio').then((m) => m.MiBarrio),
  },
  {
    path: 'municipalidad', canActivate: [municipalidadGuard],
    loadComponent: () => import('./Components/municipalidad/municipalidad').then((m) => m.Municipalidad),
  },
  {
    path: 'acerca-de', canActivate: [authGuard],
    loadComponent: () => import('./Components/acerca-de/acerca-de').then((m) => m.AcercaDe),
  },
  { path: '**', redirectTo: '' },
];