import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UserListComponent } from './user-list/user-list.component';
import { UserAddComponent } from './user-add/user-add.component';
import { UserEditComponent } from './user-edit/user-edit.component';
import { UserDetailComponent } from './user-detail/user-detail.component';
import { FormsModule } from '@angular/forms';
import {CreateOffreComponent } from './offres/offres.component';
import { OffreListComponent } from './offres-list/offres-list.component';
import { RouterModule } from '@angular/router';


@NgModule({
  declarations: [
   AppComponent,
   UserListComponent,
   UserAddComponent,
   UserDetailComponent,
   UserEditComponent,
   CreateOffreComponent,
   OffreListComponent
   
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule, 
    RouterModule
  ],
  providers: [],
  bootstrap: [AppComponent]

})
export class AppModule { }
