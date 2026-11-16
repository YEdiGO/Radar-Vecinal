import { TipoIncidente } from './reporte';

export type NivelTemperatura = 'verde' | 'amarillo' | 'naranja' | 'rojo';

export interface Barrio {
  id: string;
  nombre: string;
  poligono: [number, number][];
}

export interface TipoFrecuente {
  tipo: TipoIncidente;
  cantidad: number;
}

export interface ZonaResumen {
  id: string;
  nombre: string;
  poligono: [number, number][];
  temperatura: number;
  nivel: NivelTemperatura;
  cantidad: number;
  tipos_frecuentes: TipoFrecuente[];
  ultima_actualizacion: string;
}

export interface PuntoCaliente {
  lat: number;
  lng: number;
  temperatura: number;
  cantidad: number;
  id_barrio: string;
}