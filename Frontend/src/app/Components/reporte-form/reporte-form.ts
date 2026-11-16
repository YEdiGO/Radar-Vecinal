import { Component, inject, signal } from '@angular/core';
import { FormField, form, maxLength, minLength, required, submit, validate } from '@angular/forms/signals';
import { Router, RouterLink } from '@angular/router';
import { TIPOS } from '../../Interfaces/catalogo';
import { TipoIncidente } from '../../Interfaces/reporte';
import { mensajeError } from '../../Services/auth.interceptor';
import { ReporteService } from '../../Services/reporte.service';
import { ZonaService } from '../../Services/zona.service';
import { MapaCalor } from '../mapa-calor/mapa-calor';
import { rxResource } from '@angular/core/rxjs-interop';
import { computed } from '@angular/core';

@Component({
  selector: 'app-reporte-form',
  imports: [FormField, RouterLink, MapaCalor],
  templateUrl: './reporte-form.html',
})
export class ReporteForm {
  private reporteSvc = inject(ReporteService);
  private zonaSvc = inject(ZonaService);
  private router = inject(Router);

  tipos = TIPOS;
  zonasRes = rxResource({ stream: () => this.zonaSvc.zonas('', 30) });
  zonas = computed(() => this.zonasRes.value() ?? []);

  modelo = signal({
    tipo: 'asalto_robo' as TipoIncidente,
    descripcion: '',
    lat: null as number | null,
    lng: null as number | null,
  });

  formulario = form(this.modelo, (p) => {
    required(p.tipo, { message: 'Selecciona el tipo de incidente.' });
    required(p.descripcion, { message: 'Escribe una descripción.' });
    minLength(p.descripcion, 5, { message: 'Describe un poco más (mínimo 5 caracteres).' });
    maxLength(p.descripcion, 280, { message: 'La descripción admite hasta 280 caracteres.' });
    validate(p.descripcion, ({ value }) =>
      /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(value())
        ? { kind: 'caracteres', message: 'La descripción contiene caracteres no válidos.' }
        : undefined,
    );
    required(p.lat, { message: 'Marca el punto del incidente en el mapa.' });
    required(p.lng, { message: 'Marca el punto del incidente en el mapa.' });
  });

  error = signal('');
  cargando = signal(false);
  marcador = computed(() => {
    const { lat, lng } = this.modelo();
    return lat !== null && lng !== null ? { lat, lng } : null;
  });

  elegirPunto(p: { lat: number; lng: number }) {
    this.modelo.update((m) => ({ ...m, lat: p.lat, lng: p.lng }));
    this.formulario.lat().markAsTouched();
  }

  enviar(evento: Event) {
    evento.preventDefault();
    submit(this.formulario, async () => {
      const m = this.modelo();
      this.cargando.set(true);
      this.error.set('');
      this.reporteSvc
        .crear({ lat: m.lat!, lng: m.lng!, tipo: m.tipo, descripcion: m.descripcion })
        .subscribe({
          next: () => this.router.navigate(['/reportes']),
          error: (e) => {
            this.error.set(mensajeError(e));
            this.cargando.set(false);
          },
        });
    });
  }
}