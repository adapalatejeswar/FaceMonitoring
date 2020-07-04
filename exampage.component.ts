import { Component, OnInit } from '@angular/core';
import {Router} from  '@angular/router'


@Component({
  selector: 'app-exampage',
  templateUrl: './exampage.component.html',
  styleUrls: ['./exampage.component.scss']
})
export class ExampageComponent implements OnInit {

  constructor(private router:Router) { }

  ngOnInit() {
  }

completeExam(){
   this.router.navigate(['examcomplete']);


  }
}
