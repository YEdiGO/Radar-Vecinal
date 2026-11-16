import { Component, inject, signal } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../Services/auth.service';
import { AlertaModal } from '../alerta-modal/alerta-modal';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, RouterLinkActive, AlertaModal],
  templateUrl: './navbar.html',
})
export class Navbar {
  auth = inject(AuthService);
  abierto = signal(false);
  alertaAbierta = signal(false);
}