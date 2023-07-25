import { Component, NgModule, OnInit } from '@angular/core';
import {FormBuilder, FormControl , FormGroup } from '@angular/forms'
import { from } from 'rxjs';
import { Offre } from '../offre';
import { HttpClient } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { OffreService } from '../offre.service';

@Component({
  selector: 'app-offre',
  templateUrl: './offres.component.html',
  styleUrls: ['./offres.component.css']
})
export class CreateOffreComponent implements OnInit{
  
  offre:Offre=new Offre();
  submitted =false ;
  constructor(private offreService : OffreService,
    private router: Router ) { 
      
    }
    
ngOnInit(){}
newOffre(): void {
  this.submitted = false;
  this.offre = new Offre();
}

save() {
  this.offreService
    .createOffre(this.offre).subscribe(data => {
      console.log(data)
      this.offre = new Offre();
     
      
    },
      error => console.log(error));
}

onSubmit() {
  this.submitted = true;
  this.save();
}



  

preview:string ='';



}