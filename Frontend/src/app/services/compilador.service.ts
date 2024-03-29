import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import { Contenido } from '../models/contenido';

@Injectable({
  providedIn: 'root'
})
export class COMPILADORService {

  // API_URI = 'https://cryptic-wildwood-53384.herokuapp.com';
   //API_URI = 'http://localhost:5500';
  API_URI = 'http://44.204.42.250:5500';


  constructor(private http: HttpClient, private router: Router) { }

  COMPILAR(Contenidos: Contenido): any{
    return this.http.post<any>(`${this.API_URI}/Compilar`, Contenidos);
  }

  GRAFICAR(Contenidos: Contenido): any{
    return this.http.post<any>(`${this.API_URI}/GRAFICAR`, Contenidos);
  }

  TRADUCIR(Contenidos: Contenido): any{
    return this.http.post<any>(`${this.API_URI}/Traducir`, Contenidos);
  } 
}
