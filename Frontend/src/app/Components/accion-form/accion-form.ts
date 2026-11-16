import { Component, effect, inject, input, output, signal, untracked } from '@angular/core';
import { FormField, form, maxLength, required, submit, validate } from '@angular/forms/signals';
import { ESTADOS_ACCION, TIPOS_ACCION } from '../../Interfaces/catalogo';
import { mensajeError } from '../../Services/auth.interceptor';
import { MunicipalidadService } from '../../Services/municipalidad.service';
import { ZonaService } from '../../Services/zona.service';

@Component({
  selector: 'app-accion-form',
  imports: [FormField],
  templateUrl: './accion-form.html',
})
export class AccionForm {
  private svc = inject(MunicipalidadService);
  barrios = inject(ZonaService).barrios;

  idBarrioInicial = input('');
  guardada = output<void>();

  tiposAccion = TIPOS_ACCION;
  estados = ESTADOS_ACCION;

  modelo = signal({
    id_barrio: '',
    tipo: TIPOS_ACCION[0],
    titulo: '',
    descripcion: '',
    fecha: new Date().toISOString().slice(0, 10),
    estado: 'Planificada',
  });

  formulario = form(this.modelo, (p) => {
    required(p.id_barrio, { message: 'Selecciona un barrio.' });
    required(p.tipo, { message: 'Selecciona el tipo de acción.' });
    required(p.titulo, { message: 'Escribe un título.' });
    maxLength(p.titulo, 100, { message: 'Máximo 100 caracteres.' });
    required(p.descripcion, { message: 'Escribe una descripción.' });
    maxLength(p.descripcion, 400, { message: 'Máximo 400 caracteres.' });
    required(p.fecha, { message: 'Selecciona una fecha válida.' });
    validate(p.fecha, ({ value }) =>
      Number.isFinite(Date.parse(value())) ? undefined : { kind: 'fecha', message: 'Fecha no válida.' },
    );
    required(p.estado, { message: 'Selecciona un estado.' });
  });

  error = signal('');
  cargando = signal(false);

  constructor() {
    effect(() => {
      const id = this.idBarrioInicial();
      untracked(() => this.modelo.update((m) => ({ ...m, id_barrio: id })));
    });
  }

  guardar(evento: Event) {
    evento.preventDefault();
    submit(this.formulario, async () => {
      this.cargando.set(true);
      this.error.set('');
      this.svc.crearAccion(this.modelo()).subscribe({
        next: () => {
          this.cargando.set(false);
          this.modelo.update((m) => ({ ...m, titulo: '', descripcion: '' }));
          this.formulario().reset();
          this.guardada.emit();
        },
        error: (e) => {
          this.error.set(mensajeError(e));
          this.cargando.set(false);
        },
      });
    });
  }
}