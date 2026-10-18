export interface LessonRow { '교사명'?: string; '요일'?: string; '교시'?: string; '과목'?: string; '학급'?: string; }
export interface BridgePayload {
  tabs: string[];
  currentTab: string;
  user: string;
  role: string;
  rows: LessonRow[];
  mode: 'READ_ONLY_PREVIEW';
}
export const emptyPayload: BridgePayload = {tabs:[], currentTab:'',user:'',role:'',rows:[],mode:'READ_ONLY_PREVIEW'};
