import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CargarCasoComponent } from './cargar-caso.component';

describe('CargarCasoComponent', () => {
  let component: CargarCasoComponent;
  let fixture: ComponentFixture<CargarCasoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CargarCasoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CargarCasoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
