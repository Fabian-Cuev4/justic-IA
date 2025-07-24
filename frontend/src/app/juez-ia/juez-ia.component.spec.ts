import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JuezIaComponent } from './juez-ia.component';

describe('JuezIaComponent', () => {
  let component: JuezIaComponent;
  let fixture: ComponentFixture<JuezIaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JuezIaComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(JuezIaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
