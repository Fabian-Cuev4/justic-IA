import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MasBuscadosComponent } from './mas-buscados.component';

describe('MasBuscadosComponent', () => {
  let component: MasBuscadosComponent;
  let fixture: ComponentFixture<MasBuscadosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MasBuscadosComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MasBuscadosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
