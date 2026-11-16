import { isPlatformBrowser } from '@angular/common';
import {
  Component, ElementRef, OnDestroy, PLATFORM_ID, effect, inject, input, output, signal, viewChild,
} from '@angular/core';
import type * as Leaflet from 'leaflet';
import { COLOR_NIVEL } from '../../Interfaces/catalogo';
import { PuntoCaliente, ZonaResumen } from '../../Interfaces/zona';

const CENTRO: [number, number] = [-12.0651, -75.2049]; // Huancayo

@Component({
  selector: 'app-mapa-calor',
  template: `<div #contenedor class="mapa-contenedor" [style.height]="altura()"></div>`,
})
export class MapaCalor implements OnDestroy {
  zonas = input<ZonaResumen[]>([]);
  puntos = input<PuntoCaliente[]>([]);
  marcador = input<{ lat: number; lng: number } | null>(null);
  seleccionable = input(false);
  altura = input('65vh');

  zonaClick = output<string>();
  mapaClick = output<{ lat: number; lng: number }>();

  private contenedor = viewChild.required<ElementRef<HTMLDivElement>>('contenedor');
  private esNavegador = isPlatformBrowser(inject(PLATFORM_ID));
  private L?: typeof Leaflet;
  private mapa?: Leaflet.Map;
  private capa?: Leaflet.LayerGroup;
  private listo = signal(false);

  constructor() {
    effect(() => {
      const zonas = this.zonas();
      const puntos = this.puntos();
      const marcador = this.marcador();
      if (this.listo()) this.dibujar(zonas, puntos, marcador);
    });
    effect(() => {
      if (this.esNavegador && !this.mapa) this.iniciar();
    });
  }

  private async iniciar() {
    const modulo = await import('leaflet');
    this.L = ((modulo as any).default ?? modulo) as typeof Leaflet;
    const el = this.contenedor().nativeElement;
    if (this.mapa) return;

    this.mapa = this.L.map(el).setView(CENTRO, 14);
    this.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© Colaboradores de <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(this.mapa);
    this.capa = this.L.layerGroup().addTo(this.mapa);

    this.mapa.on('click', (e: Leaflet.LeafletMouseEvent) => {
      if (this.seleccionable()) this.mapaClick.emit({ lat: e.latlng.lat, lng: e.latlng.lng });
    });
    this.listo.set(true);
  }

  private dibujar(
    zonas: ZonaResumen[], puntos: PuntoCaliente[], marcador: { lat: number; lng: number } | null,
  ) {
    const L = this.L!;
    this.capa!.clearLayers();

    for (const z of zonas) {
      const color = COLOR_NIVEL[z.nivel];
      L.polygon(z.poligono as Leaflet.LatLngExpression[], {
        color, weight: 2, fillColor: color, fillOpacity: 0.3,
      })
        .bindTooltip(`${z.nombre} · ${z.temperatura} °`, { sticky: true })
        .on('click', () => this.zonaClick.emit(z.id))
        .addTo(this.capa!);
    }

    for (const p of puntos) {
      const intensidad = Math.min(0.7, 0.2 + p.temperatura / 25);
      L.circle([p.lat, p.lng], {
        radius: 110, stroke: false, fillColor: '#dc3545', fillOpacity: intensidad,
        interactive: false,
      }).addTo(this.capa!);
    }

    if (marcador) {
      L.circleMarker([marcador.lat, marcador.lng], {
        radius: 9, color: '#0d6efd', fillColor: '#0d6efd', fillOpacity: 0.9,
      }).addTo(this.capa!);
    }
  }

  ngOnDestroy() {
    this.mapa?.remove();
  }
}