(function(){"use strict";(function(){window.CRSETChat=window.CRSETChat||{},window.CRSETChat.init=function(t){const o=Object.assign({},{container:"#crset-chat-widget",apiUrl:"https://chat-api.crsetsolutions.com",theme:"crset-blue",position:"bottom-right"},t),n=document.querySelector(o.container);if(!n){console.error("CRSET Chat: Container não encontrado:",o.container);return}l(n,o)};function l(t,s){const o=`session_${Date.now()}_${Math.random().toString(36).substr(2,9)}`,n=`
      <div id="crset-chat-container" style="position: fixed; ${s.position==="bottom-right"?"bottom: 20px; right: 20px;":"bottom: 20px; left: 20px;"} z-index: 9999; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <!-- Botão do chat -->
        <div id="crset-chat-button" style="width: 60px; height: 60px; background: linear-gradient(135deg, #2563eb, #1d4ed8); border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); transition: all 0.3s ease;">
          <svg width="24" height="24" fill="white" viewBox="0 0 24 24">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
          </svg>
        </div>

        <!-- Janela do chat -->
        <div id="crset-chat-window" style="display: none; width: 350px; height: 500px; background: white; border-radius: 12px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15); position: absolute; bottom: 80px; right: 0; overflow: hidden;">
          <!-- Header -->
          <div style="background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; padding: 16px; display: flex; justify-content: space-between; align-items: center;">
            <div>
              <h3 style="margin: 0; font-size: 16px; font-weight: 600;">CRSET AI Assistant</h3>
              <p style="margin: 0; font-size: 12px; opacity: 0.9;">Como posso ajudar?</p>
            </div>
            <button id="crset-chat-close" style="background: none; border: none; color: white; cursor: pointer; font-size: 20px; padding: 0; width: 24px; height: 24px;">×</button>
          </div>

          <!-- Mensagens -->
          <div id="crset-chat-messages" style="height: 350px; overflow-y: auto; padding: 16px; background: #f8fafc;">
            <div style="background: white; padding: 12px; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
              <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="width: 24px; height: 24px; background: #2563eb; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 8px;">
                  <svg width="12" height="12" fill="white" viewBox="0 0 24 24">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                  </svg>
                </div>
                <span style="font-weight: 600; color: #1e293b; font-size: 14px;">CRSET Assistant</span>
              </div>
              <p style="margin: 0; color: #475569; font-size: 14px; line-height: 1.5;">Olá! 👋 Sou o assistente da CRSET Solutions. Como posso ajudá-lo hoje? Posso falar sobre os nossos serviços, planos ou fazer uma análise gratuita do seu negócio.</p>
            </div>
          </div>

          <!-- Input -->
          <div style="padding: 16px; border-top: 1px solid #e2e8f0; background: white;">
            <div style="display: flex; gap: 8px;">
              <input id="crset-chat-input" type="text" placeholder="Digite sua mensagem..." style="flex: 1; padding: 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 14px; outline: none;">
              <button id="crset-chat-send" style="background: #2563eb; color: white; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; font-size: 14px;">Enviar</button>
            </div>
          </div>
        </div>
      </div>
    `;t.innerHTML=n,p(s,o)}function p(t,s){const o=document.getElementById("crset-chat-button"),n=document.getElementById("crset-chat-window"),g=document.getElementById("crset-chat-close"),a=document.getElementById("crset-chat-input"),h=document.getElementById("crset-chat-send"),r=document.getElementById("crset-chat-messages");o.addEventListener("click",()=>{const e=n.style.display!=="none";n.style.display=e?"none":"block",e||a.focus()}),g.addEventListener("click",()=>{n.style.display="none"});function c(){const e=a.value.trim();e&&(d("user",e),a.value="",fetch(`${t.apiUrl}/api/chat`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:e,session_id:s})}).then(i=>i.json()).then(i=>{i.response?d("assistant",i.response):d("assistant","Desculpe, ocorreu um erro. Tente novamente ou contacte-nos diretamente.")}).catch(i=>{console.error("Erro na API:",i),d("assistant","Estou temporariamente indisponível. Para assistência imediata, contacte-nos em info@crsetsolutions.com ou +351 123 456 789.")}))}h.addEventListener("click",c),a.addEventListener("keypress",e=>{e.key==="Enter"&&c()});function d(e,i){const u=`
        <div style="background: white; padding: 12px; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
          <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="width: 24px; height: 24px; background: ${e==="user"?"#10b981":"#2563eb"}; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 8px;">
              <svg width="12" height="12" fill="white" viewBox="0 0 24 24">
                ${e==="user"?'<path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>':'<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>'}
              </svg>
            </div>
            <span style="font-weight: 600; color: #1e293b; font-size: 14px;">${e==="user"?"Você":"CRSET Assistant"}</span>
          </div>
          <p style="margin: 0; color: #475569; font-size: 14px; line-height: 1.5;">${i}</p>
        </div>
      `;r.insertAdjacentHTML("beforeend",u),r.scrollTop=r.scrollHeight}}document.addEventListener("DOMContentLoaded",function(){const t=document.getElementById("crset-chat-widget");t&&!t.innerHTML.trim()&&window.CRSETChat.init()})})()})();
