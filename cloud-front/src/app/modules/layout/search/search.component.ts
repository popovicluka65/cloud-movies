import { Component } from '@angular/core';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatFormField, MatInput} from "@angular/material/input";
import {MatCheckbox} from "@angular/material/checkbox";
import {MatButton} from "@angular/material/button";
import {MatDatepickerToggle, MatDateRangeInput, MatDateRangePicker} from "@angular/material/datepicker";
import {MatToolbar} from "@angular/material/toolbar";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [
    FormsModule,
    MatInput,
    MatFormField,
    MatCheckbox,
    MatButton,
    MatDateRangePicker,
    MatDatepickerToggle,
    MatDateRangeInput,
    ReactiveFormsModule,
    MatToolbar,
    NgForOf
  ],
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent {
  searchOptions: string[] = ['Title', 'Description', 'Director', 'Actor', 'Genre'];
  selectedCriteria: string = this.searchOptions[0];
  searchQuery: string = '';

  constructor() {
  }

  performSearch() {
    console.log(`Searching for ${this.searchQuery} in ${this.selectedCriteria}`);
    // Implement your search logic here
  }
}
