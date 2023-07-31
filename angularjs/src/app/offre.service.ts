import { Injectable } from '@angular/core';
import { HttpClient , HttpHeaders} from '@angular/common/http';
import { Observable ,of } from 'rxjs';
import { Offre } from './offre';
const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};
@Injectable({
  providedIn: 'root'
})
export class OffreService {

  private baseUrl = 'http://localhost:5000/api/v1/offres';

  constructor(private http: HttpClient) { }
  getOffre(id: string): Observable<any> {
    const url = `${this.baseUrl}/offre/${id}`;
    return this.http.get<Offre>(url);
  }


  createOffre(offre: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}`, offre);
  }

  updateOffre(_id: number, value: any): Observable<Object> {
    return this.http.put(`${this.baseUrl}/${_id}`, value);
  }

  deleteOffre(_id: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${_id}`,
      { responseType: 'text' });
  }
  getOffresList(): Observable<any> {
    return this.http.get(`${this.baseUrl}`);
  }
}