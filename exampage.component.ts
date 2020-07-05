import { Component, OnInit, EventEmitter } from '@angular/core';
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
  public pictureTaken = new EventEmitter<WebcamImage>();
  public showWebcam = true;
  public multipleWebcamsAvailable = false;
  public deviceId: string;
  public returnval: string;
  public intervalHandle: any;
  public videoOptions: MediaTrackConstraints = {
    // width: {ideal: 1024},
    // height: {ideal: 576}
  };

  public errors: WebcamInitError[] = [];
  public webcamImage: WebcamImage = null;
  private trigger: Subject<void> = new Subject<void>();
  loginResponse: string
  // 3 added new for monitoring - ends//

  public handleImage(webcamImage: WebcamImage): void {
    console.info('received webcam image', webcamImage);
    this.webcamImage = webcamImage;
    
  }


  // 4 added new for monitoring - starts//

  public ngOnInit(): void{
   
    WebcamUtil.getAvailableVideoInputs()
      .then((mediaDevices: MediaDeviceInfo[]) => {
        this.multipleWebcamsAvailable = mediaDevices && mediaDevices.length > 1;
      }).then(()=>{
       this.postcontinue();
      });
    
}

public postcontinue(): void{
  this.intervalHandle = 
    setInterval(()=> {
      this.trigger.next();
      let headers = new HttpHeaders({
      'Content-Type':  'application/json'
      });
    this.http.post("http://localhost:5000/faceMonitering", { img: this.webcamImage.imageAsBase64 }, {headers }).subscribe((res:any) => {
    //this.loginResponse = JSON.stringify(res)
      //  alert(this.loginResponse);  
      if (res.valid === false){
        alert(res.error);
      }
      console.log(res);
    })}, 5000); // currently interval is set for every 5 seconds.
};

public handleInitError(error: WebcamInitError): void {
  this.errors.push(error);
}
    
 
    
  
public get triggerObservable(): Observable<void> {
      return this.trigger.asObservable();
    } 

// 4 added new for monitoring - ends//

completeExam(){
  clearInterval(this.intervalHandle);
  this.router.navigate(['examcomplete']);


  }
}
