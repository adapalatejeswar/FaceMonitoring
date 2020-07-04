import { Component, OnInit } from '@angular/core';
import {Router} from  '@angular/router';
// 1 added new for monitoring - starts//
import {Subject, Observable} from 'rxjs';
import {WebcamImage, WebcamInitError, WebcamUtil} from 'ngx-webcam';
import {HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
// 1 added new for monitoring - ends//

@Component({
  selector: 'app-exampage',
  templateUrl: './exampage.component.html',
  styleUrls: ['./exampage.component.scss']
})
export class ExampageComponent implements OnInit {

  constructor(private router:Router,private http:HttpClient) { } //2 added for HTTPClient

  // 3 added new for monitoring - starts//
  public showWebcam = true;
  public multipleWebcamsAvailable = false;
  public deviceId: string;
  public returnval: string;
  public videoOptions: MediaTrackConstraints = {
    // width: {ideal: 1024},
    // height: {ideal: 576}
  };

  public errors: WebcamInitError[] = [];
  public webcamImage: WebcamImage = null;
  private trigger: Subject<void> = new Subject<void>();
  loginResponse: string
  // 3 added new for monitoring - ends//

  ngOnInit() {
    // 4 added new for monitoring - starts//
    WebcamUtil.getAvailableVideoInputs()
    .then((mediaDevices: MediaDeviceInfo[]) => {
      this.multipleWebcamsAvailable = mediaDevices && mediaDevices.length > 1;
    });
    setInterval(()=> {
      this.trigger.next();
      let headers = new HttpHeaders({
      'Content-Type':  'application/json'
      });
    this.http.post("http://localhost:5000/faceMonitering", { img: this.webcamImage.imageAsBase64 }, {headers }).subscribe(res => {
    this.loginResponse = JSON.stringify(res)
    alert(this.loginResponse);
    
    })}, 5000); // currently interval is set for every 5 seconds.
}
    // 4 added new for monitoring - ends//
  }

completeExam(){
   this.router.navigate(['examcomplete']);


  }
}
