import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import "deep-chat";
// import { DeepChat } from 'deep-chat';
import { RequestInterceptor, ResponseInterceptor } from 'deep-chat/dist/types/interceptors';
import { ChromeService } from './chrome.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  @ViewChild('chatElement') chatElementRef!: ElementRef;

  title = 'ai_connect';
  // deepChat = new DeepChat();
  currentUrl: String = "";

  constructor(private chromeService: ChromeService) {

  }
  ngOnInit() {
    this.chromeService.getCurrentTabUrl((url) => {
      this.currentUrl = url;
    })
  }
  // ngAfterViewInit(): void {
  //   // Access the native element using ElementRef
  //   const nativeElement = this.chatElementRef.nativeElement;

  //   nativeElement.initialMessages = [
  //     {
  //       html: `
  //         <div class="deep-chat-temporary-message">
  //           <button class="deep-chat-button deep-chat-suggestion-button" style="margin-top: 6px">Summarize video</button>
  //         </div>`,
  //       role: 'ai',
  //     },
  //   ];

  //   nativeElement.messageStyles = {html: {shared: {bubble: {backgroundColor: 'unset', padding: '0px'}}}};
  // }

  onButtonClick(): void {
    // Access the native element using ElementRef
    const nativeElement = this.chatElementRef.nativeElement;

    // Add the event listener
    nativeElement.onClearMessages = () => { console.log("Messages cleared"); };



    // Simulate a 'messages-cleared' event (for demonstration purposes)
    const event = new Event('messages-cleared');
    nativeElement.dispatchEvent(event);
  }

  requestInterceptor: RequestInterceptor = (details) => {
    details.body = {
      url: this.currentUrl,
      question: details.body.messages[0].text,
    }
    return details;
  }

  responseInterceptor: ResponseInterceptor = (response) => {
    if (response['text'].includes("https")) {
      return { html: `<a href=${response['text']} >Click Here to play from that time</a>` }
    } else {
      return { text: response['text'] };
    }

  };

  // clearMessages() {
  //   console.log("clearMessages");
  //   this.deepChat.clearMessages();
  // }

}
