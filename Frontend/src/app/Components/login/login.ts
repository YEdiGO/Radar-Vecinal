import { Component, inject, signal } from '@angular/core';
import { FormField, email, form, required, submit } from '@angular/forms/signals';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../Services/auth.service';
import { mensajeError } from '../../Services/auth.interceptor';

@Component({
  selector: 'app-login',
  imports: [FormField, RouterLink],
  templateUrl: './login.html',
})
export class Login {
  private auth = inject(AuthService);
  private router = inject(Router);

  modelo = signal({ correo: '', clave: '' });
  formulario = form(this.modelo, (p) => {
    required(p.correo, { message: 'Ingresa tu correo.' });
    email(p.correo, { message: 'El correo no es válido.' });
    required(p.clave, { message: 'Ingresa tu contraseña.' });
  });

  error = signal('');
  cargando = signal(false);

  ingresar(evento: Event) {
    evento.preventDefault();
    submit(this.formulario, async () => {
      this.cargando.set(true);
      this.error.set('');
      this.auth.login(this.modelo()).subscribe({
        next: () => this.router.navigate([this.auth.inicio()]),
        error: (e) => {
          this.error.set(mensajeError(e));
          this.cargando.set(false);
        },
      });
    });
  }
}