import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BaseLegalComponent } from './base-legal.component';

describe('BaseLegalComponent', () => {
  let component: BaseLegalComponent;
  let fixture: ComponentFixture<BaseLegalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BaseLegalComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BaseLegalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
