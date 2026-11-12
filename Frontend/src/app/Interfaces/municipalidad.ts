export type EstadoAccion = 'Planificada' | 'En ejecución' | 'Completada';

export interface AccionMunicipal {
  id: number;
  id_barrio: string;
  barrio_nombre: string;
  institucion: string;
  tipo: string;
  titulo: string;
  descripcion: string;
  fecha: string;
  estado: EstadoAccion;
  fecha_registro: string;
  temperatura_al_registrar: number | null;
  temperatura_al_completar: number | null;
}

export interface Estadisticas {
  vecinos_registrados: number;
  reportes_30d: number;
  reportes_falsos_pct: number;
  barrios_por_nivel: Record<string, number>;
  reportes_por_tipo: Record<string, number>;
  acciones_por_estado: Record<string, number>;
  iniciativas_por_estado: Record<string, number>;
  reduccion_promedio: number | null;
}