export type AppPersona = 'User' | 'Bot';

export interface AppMessage {
  persona: AppPersona;
  message: string;
}
