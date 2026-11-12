export type EstadoIniciativa = 'Propuesta' | 'En curso' | 'Cumplida' | 'Cancelada';

export interface Iniciativa {
  id: number;
  id_barrio: string;
  barrio_nombre: string;
  titulo: string;
  descripcion: string;
  meta: string;
  estado: EstadoIniciativa;
  fecha: string;
  participantes: number;
  temperatura_al_crear: number | null;
  temperatura_al_cumplir: number | null;
  es_mia: boolean;
  participo: boolean;
}