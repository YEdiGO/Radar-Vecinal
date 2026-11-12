import { Component, inject, signal } from '@angular/core';
import { FormField, form, maxLength, required, submit } from '@angular/forms/signals';
import { Router, RouterLink } from '@angular/router';
import { mensajeError } from '../../Services/auth.interceptor';
import { AuthService } from '../../Services/auth.service';
import { IniciativaService } from '../../Services/iniciativa.service';
import { ZonaService } from '../../Services/zona.service';

@Component({
  selector: 'app-iniciativa-form',
  imports: [FormField, RouterLink],
  templateUrl: './iniciativa-form.html',
})
export class IniciativaForm {
  private svc = inject(IniciativaService);
  private router = inject(Router);
  barrios = inject(ZonaService).barrios;

  modelo = signal({
    id_barrio: inject(AuthService).usuario()?.id_barrio ?? '',
    titulo: '',
    descripcion: '',
    meta: '',
  });

  formulario = form(this.modelo, (p) => {
    required(p.id_barrio, { message: 'Elige un barrio.' });
    required(p.titulo, { message: 'Escribe un título.' });
    maxLength(p.titulo, 100, { message: 'Máximo 100 caracteres.' });
    required(p.descripcion, { message: 'Escribe una descripción.' });
    maxLength(p.descripcion, 400, { message: 'Máximo 400 caracteres.' });
    required(p.meta, { message: 'Escribe una meta.' });
    maxLength(p.meta, 200, { message: 'Máximo 200 caracteres.' });
  });

  error = signal('');
  cargando = signal(false);

  guardar(evento: Event) {
    evento.preventDefault();
    submit(this.formulario, async () => {
      this.cargando.set(true);
      this.error.set('');
      this.svc.crear(this.modelo()).subscribe({
        next: () => this.router.navigate(['/iniciativas']),
        error: (e) => {
          this.error.set(mensajeError(e));
          this.cargando.set(false);
        },
      });
    });
  }
}