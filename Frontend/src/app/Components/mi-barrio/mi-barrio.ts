import { DatePipe } from '@angular/common';
import { Component, computed, inject } from '@angular/core';
import { rxResource } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { BADGE_NIVEL, ETIQUETA_NIVEL, ETIQUETA_TIPO } from '../../Interfaces/catalogo';
import { AuthService } from '../../Services/auth.service';
import { IniciativaService } from '../../Services/iniciativa.service';
import { MunicipalidadService } from '../../Services/municipalidad.service';
import { ZonaService } from '../../Services/zona.service';

@Component({
  selector: 'app-mi-barrio',
  imports: [DatePipe, RouterLink],
  templateUrl: './mi-barrio.html',
})
export class MiBarrio {
  private zonaSvc = inject(ZonaService);
  private muniSvc = inject(MunicipalidadService);
  private iniSvc = inject(IniciativaService);
  usuario = inject(AuthService).usuario;

  etiquetaTipo = ETIQUETA_TIPO;
  etiquetaNivel = ETIQUETA_NIVEL;
  badge = BADGE_NIVEL;

  idBarrio = computed(() => this.usuario()?.id_barrio ?? '');

  z30 = rxResource({ stream: () => this.zonaSvc.zonas('', 30) });
  z7 = rxResource({ stream: () => this.zonaSvc.zonas('', 7) });
  accionesRes = rxResource({
    params: () => this.idBarrio(),
    stream: ({ params }) => this.muniSvc.acciones({ idBarrio: params }),
  });
  iniciativasRes = rxResource({
    params: () => this.idBarrio(),
    stream: ({ params }) => this.iniSvc.listar(params),
  });

  zona = computed(() => this.z30.value()?.find((z) => z.id === this.idBarrio()) ?? null);
  reportes7 = computed(() => this.z7.value()?.find((z) => z.id === this.idBarrio())?.cantidad ?? 0);
  acciones = computed(() => this.accionesRes.value() ?? []);
  iniciativas = computed(() => (this.iniciativasRes.value() ?? []).slice(0, 3));

  nombreBarrio = computed(
    () => this.zonaSvc.barrios().find((b) => b.id === this.idBarrio())?.nombre ?? '',
  );
}