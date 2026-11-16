import { Component, computed, inject, signal } from '@angular/core';
import { rxResource } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { EstadoIniciativa, Iniciativa } from '../../Interfaces/iniciativa';
import { mensajeError } from '../../Services/auth.interceptor';
import { AuthService } from '../../Services/auth.service';
import { IniciativaService } from '../../Services/iniciativa.service';

@Component({
  selector: 'app-iniciativas',
  imports: [RouterLink],
  templateUrl: './iniciativas.html',
})
export class Iniciativas {
  private svc = inject(IniciativaService);
  auth = inject(AuthService);

  error = signal('');
  res = rxResource({ stream: () => this.svc.listar() });
  iniciativas = computed(() => this.res.value() ?? []);

  badge(e: EstadoIniciativa) {
    return {
      Propuesta: 'text-bg-secondary', 'En curso': 'text-bg-primary',
      Cumplida: 'text-bg-success', Cancelada: 'text-bg-dark',
    }[e];
  }

  participar(i: Iniciativa) {
    this.svc.participar(i.id).subscribe({
      next: () => this.res.reload(),
      error: (e) => this.error.set(mensajeError(e)),
    });
  }

  cambiarEstado(i: Iniciativa, estado: EstadoIniciativa) {
    this.svc.cambiarEstado(i.id, estado).subscribe({
      next: () => this.res.reload(),
      error: (e) => this.error.set(mensajeError(e)),
    });
  }
}