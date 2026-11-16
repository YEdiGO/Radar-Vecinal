import { DatePipe } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { rxResource } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { ETIQUETA_TIPO } from '../../Interfaces/catalogo';
import { Reporte } from '../../Interfaces/reporte';
import { mensajeError } from '../../Services/auth.interceptor';
import { AuthService } from '../../Services/auth.service';
import { ReporteService } from '../../Services/reporte.service';

@Component({
  selector: 'app-reportes',
  imports: [DatePipe, RouterLink],
  templateUrl: './reportes.html',
})
export class Reportes {
  private svc = inject(ReporteService);
  private auth = inject(AuthService);

  etiquetaTipo = ETIQUETA_TIPO;
  vista = signal<'barrio' | 'mios'>('barrio');
  error = signal('');

  res = rxResource({
    params: () => this.vista(),
    stream: ({ params }) =>
      this.svc.listar(
        params === 'mios'
          ? { soloMios: true }
          : { idBarrio: this.auth.usuario()?.id_barrio ?? undefined },
      ),
  });
  reportes = computed(() => this.res.value() ?? []);

  badge(estado: Reporte['estado']) {
    return {
      activo: 'text-bg-secondary', confirmado: 'text-bg-success',
      falso: 'text-bg-danger', archivado: 'text-bg-dark',
    }[estado];
  }

  votar(r: Reporte, tipo: 'confirmo' | 'incorrecto') {
    this.error.set('');
    this.svc.votar(r.id, tipo).subscribe({
      next: () => this.res.reload(),
      error: (e) => this.error.set(mensajeError(e)),
    });
  }

  eliminar(r: Reporte) {
    if (!confirm('¿Eliminar este reporte?')) return;
    this.svc.eliminar(r.id).subscribe({
      next: () => this.res.reload(),
      error: (e) => this.error.set(mensajeError(e)),
    });
  }
}