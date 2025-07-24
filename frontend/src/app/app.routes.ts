import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { BaseLegalComponent } from './base-legal/base-legal.component';
import { HistorialCasosComponent } from './historial-casos/historial-casos.component';
import { MasBuscadosComponent } from './mas-buscados/mas-buscados.component';
import { JuezIaComponent } from './juez-ia/juez-ia.component';
import { CargarCasoComponent } from './cargar-caso/cargar-caso.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'inicio',
    pathMatch: 'full',
  },
  {
    path: 'inicio',
    component: HomeComponent,
  },
  { path: 'base-legal', component: BaseLegalComponent },
  { path: 'historial-casos', component: HistorialCasosComponent },
  { path: 'mas-buscados', component: MasBuscadosComponent },
  { path: 'juez-ia', component: JuezIaComponent },
  { path: 'cargar-caso', component: CargarCasoComponent},
  {
    path: '**',
    redirectTo: 'inicio',
    pathMatch: 'full',
  },

];
