export type Rol = 'vecino' | 'municipalidad';

export interface Usuario {
  id: number;
  nombre: string;
  correo: string;
  rol: Rol;
  id_barrio: string | null;
  institucion: string | null;
  fecha_registro: string;
}

export interface TokenRespuesta {
  access_token: string;
  token_type: string;
  usuario: Usuario;
}