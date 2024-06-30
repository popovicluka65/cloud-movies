import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadMovieComponent } from './upload-movie.component';

describe('UploadMovieComponent', () => {
  let component: UploadMovieComponent;
  let fixture: ComponentFixture<UploadMovieComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UploadMovieComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UploadMovieComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
