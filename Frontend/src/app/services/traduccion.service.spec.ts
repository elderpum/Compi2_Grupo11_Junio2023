import { TestBed } from '@angular/core/testing';

import { TraduccionService } from './traduccion.service';

describe('IndexService', () => {
  let service: TraduccionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TraduccionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});