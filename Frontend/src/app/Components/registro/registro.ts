import { Component, inject, signal } from '@angular/core';
import {
  FormField, email, form, maxLength, minLength, required, submit, validate,
} from '@angular/forms/signals';
import { Router, RouterLink } from '@angular/router';
import { mensajeError } from '../../Services/auth.interceptor';
import { AuthService } from '../../Services/auth.service';
import { ZonaService } from '../../Services/zona.service';

@Component({
  selector: 'app-registro',
  imports: [FormField, RouterLink],
  templateUrl: './registro.html',
})
export class Registro {
  private auth = inject(AuthService);
  private router = inject(Router);
  barrios = inject(ZonaService).barrios;

  modelo = signal({ nombre: '', correo: '', clave: '', confirmar: '', id_barrio: '' });
  formulario = form(this.modelo, (p) => {
    required(p.nombre, { message: 'Ingresa tu nombre.' });
    minLength(p.nombre, 2, { message: 'Mínimo 2 caracteres.' });
    maxLength(p.nombre, 80, { message: 'Máximo 80 caracteres.' });
    required(p.correo, { message: 'Ingresa tu correo.' });
    email(p.correo, { message: 'El correo no es válido.' });
    required(p.clave, { message: 'Crea una contraseña.' });
    minLength(p.clave, 6, { message: 'Mínimo 6 caracteres.' });
    maxLength(p.clave, 72, { message: 'Máximo 72 caracteres.' });
    required(p.confirmar, { message: 'Confirma tu contraseña.' });
    validate(p.confirmar, ({ value, valueOf }) =>
      value() !== valueOf(p.clave) ? { kind: 'noCoincide', message: 'Las contraseñas no coinciden.' } : undefined,
    );
    required(p.id_barrio, { message: 'Selecciona tu barrio.' });
  });

  error = signal('');
  cargando = signal(false);

  registrar(evento: Event) {
    evento.preventDefault();
    submit(this.formulario, async () => {
      const { nombre, correo, clave, id_barrio } = this.modelo();
      this.cargando.set(true);
      this.error.set('');
      this.auth.registro({ nombre, correo, clave, id_barrio }).subscribe({
        next: () => this.router.navigate(['/']),
        error: (e) => {
          this.error.set(mensajeError(e));
          this.cargando.set(false);
        },
      });
    });
  }
}