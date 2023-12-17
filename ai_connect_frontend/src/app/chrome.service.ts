import { Injectable } from '@angular/core';

declare const chrome: any;

@Injectable({
  providedIn: 'root',
})
export class ChromeService {
  getCurrentTabUrl(callback: (url: string) => void): void {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs: any[]) => {
      const url = tabs[0].url;
      callback(url);
    });
  }
}