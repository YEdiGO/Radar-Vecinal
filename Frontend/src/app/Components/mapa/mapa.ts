import { Component, OnDestroy, computed, inject, signal } from '@angular/core';
import { rxResource } from '@angular/core/rxjs-interop';
import { FormField, form } from '@angular/forms/signals';
import { RouterLink } from '@angular/router';
import { Alerta } from '../../Interfaces/alerta';
import {
  BADGE_NIVEL, COLOR_NIVEL, ETIQUETA_NIVEL, ETIQUETA_TIPO, TIPOS,
} from '../../Interfaces/catalogo';
import { AlertaService } from '../../Services/alerta.service';
import { AuthService } from '../../Services/auth.service';
import { ZonaService } from '../../Services/zona.service';
import { MapaCalor } from '../mapa-calor/mapa-calor';

@Component({
  selector: 'app-mapa',
  imports: [FormField, RouterLink, MapaCalor],
  templateUrl: './mapa.html',
})
export class Mapa implements OnDestroy {
  auth = inject(AuthService);
  private zonaSvc = inject(ZonaService);
  private alertaSvc = inject(AlertaService);

  tipos = TIPOS;
  etiquetaTipo = ETIQUETA_TIPO;
  etiquetaNivel = ETIQUETA_NIVEL;
  badge = BADGE_NIVEL;
  color = COLOR_NIVEL;

  filtros = form(signal({ tipo: '', dias: '30' }));

  zonasRes = rxResource({
    params: () => ({ tipo: this.filtros.tipo().value(), dias: +this.filtros.dias().value() }),
    stream: ({ params }) => this.zonaSvc.zonas(params.tipo, params.dias),
  });
  puntosRes = rxResource({
    params: () => +this.filtros.dias().value(),
    stream: ({ params }) => this.zonaSvc.puntos(params),
  });

  zonas = computed(() => this.zonasRes.value() ?? []);
  puntos = computed(() => this.puntosRes.value() ?? []);

  seleccionId = signal<string | null>(null);
  seleccion = computed(() => this.zonas().find((z) => z.id === this.seleccionId()) ?? null);

  alertas = signal<Alerta[]>([]);
  private timer: ReturnType<typeof setInterval>;

  constructor() {
    this.cargarAlertas();
    this.timer = setInterval(() => this.cargarAlertas(), 30_000);
  }

  private cargarAlertas() {
    this.alertaSvc.activas().subscribe({ next: (a) => this.alertas.set(a), error: () => {} });
  }

  minutos(seg: number) {
    return Math.max(1, Math.ceil(seg / 60));
  }

  ngOnDestroy() {
    clearInterval(this.timer);
  }
}