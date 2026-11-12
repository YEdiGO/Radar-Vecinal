export interface Alerta {
  id: number;
  id_barrio: string;
  barrio_nombre: string;
  motivo: string;
  ubicacion: string;
  inicio: string;
  expira: string;
  segundos_restantes: number;
}