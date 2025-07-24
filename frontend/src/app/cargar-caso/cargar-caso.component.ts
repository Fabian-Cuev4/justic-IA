import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { QueryService } from '../services/query.service';
import { Caso } from '../models/question-request';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-cargar-caso',
  templateUrl: './cargar-caso.component.html',
  imports: [FormsModule, ReactiveFormsModule, RouterModule],
  styleUrl: './cargar-caso.component.css',
})
export class CargarCasoComponent {
  casoForm: FormGroup;
  pdfFile: File | null = null;
  tiposDelito = [
    { value: 'cibernetico', label: 'Delito cibernético' },
    { value: 'fraude', label: 'Delito de fraude' },
    { value: 'corrupcion', label: 'Corrupción' },
    { value: 'violencia', label: 'Violencia' },
    // Agrega más tipos si es necesario
  ];
  enviado = false;
  loading: boolean = false;
  errorMsg = '';

  constructor(
    private readonly fb: FormBuilder,
    private readonly queryService: QueryService,
    private readonly router: Router
  ) {
    this.casoForm = this.fb.group({
      nombre: ['', [Validators.required]],
      tipoDelito: ['', Validators.required],
      partePolicial: [null, Validators.required],
    });
  }

  onFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      if (file.type === 'application/pdf') {
        this.pdfFile = file;
        this.casoForm.patchValue({ partePolicial: file });
        this.errorMsg = '';
      } else {
        this.pdfFile = null;
        this.casoForm.patchValue({ partePolicial: null });
        this.errorMsg = 'El archivo debe ser un PDF.';
      }
    }
  }

  submitCaso() {
    this.enviado = true;
    if (this.casoForm.invalid || !this.pdfFile) {
      this.errorMsg = 'Por favor complete todos los campos y adjunte un PDF.';
      return;
    }
    const formData = new FormData();
    formData.append('partePolicial', this.pdfFile);
    let caso: Caso = {
      nombre: this.casoForm.value.nombre,
      tipoDelito: this.casoForm.value.tipoDelito,
    };
    this.loading = true;
    this.queryService.nuevoCaso(caso, this.pdfFile).subscribe({
      next: () => {
        this.casoForm.reset();
        this.pdfFile = null;
        this.enviado = false;
        this.errorMsg = '';
        this.router.navigate(['/juez-ia']);
      },
      error: (err) => {
        this.errorMsg = 'Error al enviar el caso.';
      },
      complete: () => {
        this.loading = false;
      }
    });
  }
}
