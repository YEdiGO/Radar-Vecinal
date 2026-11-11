import { Component, inject, output, signal } from '@angular/core';
import { FormField, form, required, submit } from '@angular/forms/signals';
import { MOTIVOS_ALERTA } from '../../Interfaces/catalogo';
import { AlertaService } from '../../Services/alerta.service';
import { mensajeError } from '../../Services/auth.interceptor';
import { AuthService } from '../../Services/auth.service';
import { ZonaService } from '../../Services/zona.service';

@Component({
  selector: 'app-alerta-modal',
  imports: [FormField],
  templateUrl: './alerta-modal.html',
})
export class AlertaModal {
  private svc = inject(AlertaService);
  barrios = inject(ZonaService).barrios;
  motivos = MOTIVOS_ALERTA;
  cerrar = output<void>();

  modelo = signal({
    id_barrio: inject(AuthService).usuario()?.id_barrio ?? '',
    motivo: MOTIVOS_ALERTA[0],
    ubicacion: '',
  });

  formulario = form(this.modelo, (p) => {
    required(p.id_barrio, { message: 'Selecciona el sector.' });
    required(p.motivo, { message: 'Selecciona el motivo.' });
  });

  error = signal('');
  enviada = signal(false);
  cargando = signal(false);

  transmitir(evento: Event) {
    evento.preventDefault();
    submit(this.formulario, async () => {
      this.cargando.set(true);
      this.error.set('');
      this.svc.crear(this.modelo()).subscribe({
        next: () => {
          this.enviada.set(true);
          this.cargando.set(false);
        },
        error: (e) => {
          this.error.set(mensajeError(e));
          this.cargando.set(false);
        },
      });
    });
  }
}