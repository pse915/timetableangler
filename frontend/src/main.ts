import {bootstrapApplication} from '@angular/platform-browser';
import {AppComponent} from './app/app.component';
import {connectStreamlit} from './app/bridge';
bootstrapApplication(AppComponent).then(() => connectStreamlit()).catch(err => {
  console.error('Angular preview bootstrap failed', err);
  const root=document.querySelector('app-root');
  if (root) root.textContent='미리보기 시작 중 오류가 발생했습니다. 기존 Streamlit 화면을 사용하세요.';
});
