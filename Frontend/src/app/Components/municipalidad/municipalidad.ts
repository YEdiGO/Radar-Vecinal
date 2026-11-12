import { DatePipe } from '@angular/common';
import { Component, computed, inject, signal } from '@angular/core';
import { rxResource } from '@angular/core/rxjs-interop';
import { BADGE_NIVEL, ETIQUETA_NIVEL, ETIQUETA_TIPO } from '../../Interfaces/catalogo';
import { AccionMunicipal } from '../../Interfaces/municipalidad';
import { Reporte } from '../../Interfaces/reporte';
import { mensajeError } from '../../Services/auth.interceptor';
import { MunicipalidadService } from '../../Services/municipalidad.service';
import { ReporteService } from '../../Services/reporte.service';
import { AccionForm } from '../accion-form/accion-form';

type Pestana = 'criticos' | 'acciones' | 'moderacion' | 'estadisticas';

@Component({
  selector: 'app-municipalidad',
  imports: [DatePipe, AccionForm],
  templateUrl: './municipalidad.html',
})
export class Municipalidad {
  private svc = inject(MunicipalidadService);
  private reporteSvc = inject(ReporteService);

  etiquetaTipo = ETIQUETA_TIPO;
  etiquetaNivel = ETIQUETA_NIVEL;
  badge = BADGE_NIVEL;

  pestana = signal<Pestana>('criticos');
  barrioParaAccion = signal('');
  error = signal('');

  criticosRes = rxResource({ stream: () => this.svc.criticos() });
  accionesRes = rxResource({ stream: () => this.svc.acciones({ soloMias: true }) });
  reportesRes = rxResource({ stream: () => this.reporteSvc.listar({ limite: 60 }) });
  statsRes = rxResource({ stream: () => this.svc.estadisticas() });

  criticos = computed(() => this.criticosRes.value() ?? []);
  acciones = computed(() => this.accionesRes.value() ?? []);
  reportes = computed(() => this.reportesRes.value() ?? []);
  stats = computed(() => this.statsRes.value() ?? null);

  tiposStats = computed(() => Object.entries(this.stats()?.reportes_por_tipo ?? {}));
  nivelesStats = computed(() => Object.entries(this.stats()?.barrios_por_nivel ?? {}));

  registrarEn(idBarrio: string) {
    this.barrioParaAccion.set(idBarrio);
    this.pestana.set('acciones');
  }

  accionGuardada() {
    this.accionesRes.reload();
    this.criticosRes.reload();
    this.statsRes.reload();
  }

  cambiarEstado(a: AccionMunicipal, estado: 'En ejecución' | 'Completada') {
    this.svc.cambiarEstadoAccion(a.id, estado).subscribe({
      next: () => this.accionGuardada(),
      error: (e) => this.error.set(mensajeError(e)),
    });
  }

  moderar(r: Reporte, estado: 'activo' | 'falso' | 'archivado') {
    this.reporteSvc.moderar(r.id, estado).subscribe({
      next: () => {
        this.reportesRes.reload();
        this.criticosRes.reload();
      },
      error: (e) => this.error.set(mensajeError(e)),
    });
  }

  badgeEstado(e: string) {
    return e === 'Completada' ? 'text-bg-success' : e === 'En ejecución' ? 'text-bg-primary' : 'text-bg-secondary';
  }
}