import { Component , OnInit } from '@angular/core';
import { Offre } from '../offre';
import { ActivatedRoute, Router } from '@angular/router';
import { OffreService } from '../offre.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-offres-list',
  templateUrl: './offres-list.component.html',
  styleUrls: ['./offres-list.component.css']
})
export class OffreListComponent implements OnInit {
  offers: Observable<Offre[]>|any;
constructor(private route :Router, private offreService:OffreService){}
ngOnInit() {
  this.reloadData();
}

reloadData() {
  this.offers = this.offreService.getOffresList();
}

deleteOffer(_id: string) {
  this.offreService.deleteOffre(_id)
    .subscribe(
      data => {
        console.log(data);
        this.reloadData();
      },
      error => console.log(error));
}
updateOffer(id: string) {
  this.route.navigate(['update', id]);
}
OfferDetail(_id: string) {
  this.route.navigate(['details', _id]);
}
}