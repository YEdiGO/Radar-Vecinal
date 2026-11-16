export type TipoIncidente =
  | 'asalto_robo' | 'pandillaje' | 'alcohol_drogas'
  | 'falta_alumbrado' | 'actividad_sospechosa' | 'otro';

export type EstadoReporte = 'activo' | 'confirmado' | 'falso' | 'archivado';

export interface Reporte {
  id: number;
  lat: number;
  lng: number;
  id_barrio: string;
  barrio_nombre: string;
  tipo: TipoIncidente;
  gravedad: number;
  descripcion: string;
  fecha: string;
  estado: EstadoReporte;
  moderado: boolean;
  confirmaciones: number;
  incorrectos: number;
  es_mio: boolean;
  mi_voto: 'confirmo' | 'incorrecto' | null;
}