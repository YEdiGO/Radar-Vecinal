import { TipoIncidente } from './reporte';
import { NivelTemperatura } from './zona';

export const TIPOS: { valor: TipoIncidente; etiqueta: string }[] = [
  { valor: 'asalto_robo', etiqueta: 'Asalto o robo' },
  { valor: 'pandillaje', etiqueta: 'Pandillaje' },
  { valor: 'alcohol_drogas', etiqueta: 'Zona de consumo de alcohol o drogas' },
  { valor: 'falta_alumbrado', etiqueta: 'Falta de alumbrado' },
  { valor: 'actividad_sospechosa', etiqueta: 'Actividad sospechosa' },
  { valor: 'otro', etiqueta: 'Otro' },
];

export const ETIQUETA_TIPO: Record<string, string> = Object.fromEntries(
  TIPOS.map((t) => [t.valor, t.etiqueta]),
);

export const COLOR_NIVEL: Record<NivelTemperatura, string> = {
  verde: '#198754', amarillo: '#ffc107', naranja: '#fd7e14', rojo: '#dc3545',
};

export const ETIQUETA_NIVEL: Record<NivelTemperatura, string> = {
  verde: 'Tranquila', amarillo: 'Atención', naranja: 'Alerta', rojo: 'Crítica',
};

export const BADGE_NIVEL: Record<NivelTemperatura, string> = {
  verde: 'text-bg-success', amarillo: 'text-bg-warning',
  naranja: 'text-bg-orange', rojo: 'text-bg-danger',
};

export const TIPOS_ACCION = [
  'Patrullaje de serenazgo', 'Operativo con la policía', 'Alumbrado',
  'Campaña de prevención', 'Otro',
];

export const ESTADOS_ACCION = ['Planificada', 'En ejecución', 'Completada'];

export const MOTIVOS_ALERTA = [
  'Asalto en curso / Arrebato', 'Robo a vivienda forzada',
  'Violencia o riña callejera', 'Accidente / Incendio',
];