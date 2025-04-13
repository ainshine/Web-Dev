export interface Company {
    id: number;
    name: string;
    description: string;
    city: string;
    address: string;
  }
  export interface Vacancy {
    id: number;
    name: string;
    description: string;
    salary: number;
    company: number;
  }
  import { Injectable } from '@angular/core';
  import { HttpClient } from '@angular/common/http';
  import { Company } from './company';
  import { Observable } from 'rxjs';
  
  @Injectable({
    providedIn: 'root'
  })
  export class CompanyService {
    BASE_URL = 'http://localhost:8000/api';
  
    constructor(private client: HttpClient) {}
  
    getCompanies(): Observable<Company[]> {
      return this.client.get<Company[]>(`${this.BASE_URL}/companies/`);
    }
  
    getCompanyVacancies(id: number): Observable<any> {
      return this.client.get(`${this.BASE_URL}/companies/${id}/vacancies/`);
    }
  }
  import { Component, OnInit } from '@angular/core';
import { CompanyService } from '../company.service';
import { Company } from '../company';

@Component({
  selector: 'app-company-list',
  templateUrl: './company-list.component.html'
})
export class CompanyListComponent implements OnInit {
  companies: Company[] = [];
  selectedCompanyId: number | null = null;
  vacancies: any[] = [];

  constructor(private companyService: CompanyService) {}

  ngOnInit(): void {
    this.companyService.getCompanies().subscribe(data => {
      this.companies = data;
    });
  }

  showVacancies(id: number): void {
    this.selectedCompanyId = id;
    this.companyService.getCompanyVacancies(id).subscribe(data => {
      this.vacancies = data;
    });
  }
}  