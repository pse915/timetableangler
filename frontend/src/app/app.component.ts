import {CommonModule} from '@angular/common';
import {ChangeDetectionStrategy, Component, HostListener, computed, signal} from '@angular/core';
import {payload, navigate, resizeFrame} from './bridge';
import {LessonRow} from './types';
@Component({
  selector: 'app-root', standalone: true, imports: [CommonModule],
  templateUrl: './app.component.html', styleUrls: ['./app.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppComponent {
  readonly data = payload;
  readonly search = signal('');
  readonly selected = signal<LessonRow|null>(null);
  readonly rows = computed(() => {
    const value = this.search().trim().toLowerCase();
    const all = this.data().rows;
    if (!value) return all;
    return all.filter(row => Object.values(row).some(v => String(v??'').toLowerCase().includes(value)));
  });
  selectTab(tab: string): void {
    if (!this.data().tabs.includes(tab)) return;
    navigate(tab);
  }
  setSearch(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.search.set(target.value);
  }
  open(row: LessonRow): void { this.selected.set(row); resizeFrame(); }
  close(): void { this.selected.set(null); resizeFrame(); }
  @HostListener('document:keydown.escape') onEscape(): void {this.close();}
}
