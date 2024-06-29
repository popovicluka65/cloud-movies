import {AfterViewInit, Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {MovieService} from "../movie.service";

@Component({
  selector: 'app-movie-details',
  standalone: true,
  imports: [],
  templateUrl: './movie-details.component.html',
  styleUrl: './movie-details.component.css'
})
export class MovieDetailsComponent implements AfterViewInit{

  @ViewChild('videoPlayer') videoPlayer!: ElementRef;
  //videoUrl: string = 'https://content-bucket-cloud-app-movie2.s3.amazonaws.com/movies/Juzni%20vetar?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA6ODU7KB4FIOWQUXF%2F20240629%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Date=20240629T193340Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHwaDGV1LWNlbnRyYWwtMSJHMEUCIQDO9rXXD%2BVoe3oP%2BIHgrOLFnEpjzHt%2Fsf0b5k6FOngf%2FAIgbExQHiW3NcYwmoZ2d5GvVMhjjBbRkPYeDEWT0HBNypIq%2BQIINRAAGgw5OTIzODI3NjcyMjQiDHLwCFBomNE%2Bac0k1irWAiyAO1%2Br1P3%2FJazrB5TYhCtA1iRXTf12dHhlc5WShIZZYL5QJcOXt9%2F%2BIQU4gYX0x1Gwmzd%2FZR6i0n4Ch2J1T7gLU7fUnNTnG3QV44sw4sMa1fn07kCF6nFRplPyQTBr%2BTRaGqmlBEEt2DXtKpllpPJ%2FC95qFLpGlzDD0ktSopzhqSwiPBcyGa7T1bTE5tBDdmVYlv%2FXwO%2BZR1Eb2uVV7fmsg%2Buj0ysajIiMaH3ewEvhlPJ7ig86g9FBkm305jfi780iSqimvL5f4G0c0aMzCSr6RXm4l62FDXg2RqhCqu%2FiF0I92TltY5r9Sc%2FD7xr6L1qqFAn%2B8I6Yfa7hHKNNPtQt2xZS9zP9u2ltVU7cp8rTTvb3IY2DyWk%2B1jh6%2BlJ64u0ZSl%2Fr3FgDv5ZaZ9TUQ2QaHWncyPxRCm4p2gk3xEaplVd6Nygp6vXI5QJ0Q0ReUwx5Kd%2BPLTCowoG0BjqeAZzkp0E869MeQyHWue5JO2V1iVNGUzZA6EuAAtb2mYEwZX50mHtSNtMcBLuhggi0RvyeIhNNvj6VaK5ihfNreSyoaJ7fhiqdiweTuzsNs193bvElZRxZbrapjgIo%2Bll%2Fc%2F%2FQk192fX25OUuxEddEog1cdAusXnNVIRxF6%2FPI9CzyY7IYYP6I8pfp5Dw9wZ06mbO1vBDriFw%2F01Ti7Hha&X-Amz-Signature=eef731f0801f83252349fff3ab8e664693a150120235a62a18e6070ac75c4050';
  videoUrl: string = ''; // Inicijalno prazan string za video URL
  constructor(private movieService:MovieService) {}
  ngAfterViewInit(): void {
    this.getMovie();
  }

  getMovie() {
    //dobaviti ga prvo preko service
    // this.movieService.getMovie("Juzni vetar").subscribe(
    //   (movie: string) => {
    //     console.log('Received movie:', movie);
    //     this.videoUrl = movie;
    //     this.playVideo();
    //   },
    //   (error) => {
    //     console.error('Error fetching movie:', error);
    //   }
    // );

    this.videoUrl = 'https://content-bucket-cloud-app-movie2.s3.amazonaws.com/movies/Juzni%20vetar?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA6ODU7KB4FIOWQUXF%2F20240629%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Date=20240629T193340Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHwaDGV1LWNlbnRyYWwtMSJHMEUCIQDO9rXXD%2BVoe3oP%2BIHgrOLFnEpjzHt%2Fsf0b5k6FOngf%2FAIgbExQHiW3NcYwmoZ2d5GvVMhjjBbRkPYeDEWT0HBNypIq%2BQIINRAAGgw5OTIzODI3NjcyMjQiDHLwCFBomNE%2Bac0k1irWAiyAO1%2Br1P3%2FJazrB5TYhCtA1iRXTf12dHhlc5WShIZZYL5QJcOXt9%2F%2BIQU4gYX0x1Gwmzd%2FZR6i0n4Ch2J1T7gLU7fUnNTnG3QV44sw4sMa1fn07kCF6nFRplPyQTBr%2BTRaGqmlBEEt2DXtKpllpPJ%2FC95qFLpGlzDD0ktSopzhqSwiPBcyGa7T1bTE5tBDdmVYlv%2FXwO%2BZR1Eb2uVV7fmsg%2Buj0ysajIiMaH3ewEvhlPJ7ig86g9FBkm305jfi780iSqimvL5f4G0c0aMzCSr6RXm4l62FDXg2RqhCqu%2FiF0I92TltY5r9Sc%2FD7xr6L1qqFAn%2B8I6Yfa7hHKNNPtQt2xZS9zP9u2ltVU7cp8rTTvb3IY2DyWk%2B1jh6%2BlJ64u0ZSl%2Fr3FgDv5ZaZ9TUQ2QaHWncyPxRCm4p2gk3xEaplVd6Nygp6vXI5QJ0Q0ReUwx5Kd%2BPLTCowoG0BjqeAZzkp0E869MeQyHWue5JO2V1iVNGUzZA6EuAAtb2mYEwZX50mHtSNtMcBLuhggi0RvyeIhNNvj6VaK5ihfNreSyoaJ7fhiqdiweTuzsNs193bvElZRxZbrapjgIo%2Bll%2Fc%2F%2FQk192fX25OUuxEddEog1cdAusXnNVIRxF6%2FPI9CzyY7IYYP6I8pfp5Dw9wZ06mbO1vBDriFw%2F01Ti7Hha&X-Amz-Signature=eef731f0801f83252349fff3ab8e664693a150120235a62a18e6070ac75c4050';
    this.playVideo();
  }

  playVideo() {
    const videoElement = this.videoPlayer.nativeElement;
    videoElement.src = this.videoUrl;
    videoElement.load();
    videoElement.play();
  }

}
