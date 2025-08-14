import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.chat import chat_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuração para Render
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'crset-ai-assistant-secret-key-2025')

# Configurar CORS para domínios CRSET
cors_origins = os.getenv('CORS_ORIGINS', 'https://crsetsolutions.com,https://chat.crsetsolutions.com').split(',')
CORS(app, origins=cors_origins, supports_credentials=True)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')

# Database configuration
database_url = os.getenv('DATABASE_URL')
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# Rota específica para ficheiros estáticos (DEVE VIR ANTES da catch-all)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Endpoint direto para widget.js (solução robusta)
@app.route('/api/widget.js')
def serve_widget_direct():
    widget_content = """
// CRSET AI Assistant Widget - Standalone Version
(function() {
  'use strict';
  
  window.CRSETChat = window.CRSETChat || {};
  
  window.CRSETChat.init = function(config) {
    const defaultConfig = {
      container: '#crset-chat-widget',
      apiUrl: 'https://crset-ai-assistant-backend-production.up.railway.app',
      theme: 'crset-blue',
      position: 'bottom-right'
    };
    
    const settings = Object.assign({}, defaultConfig, config);
    const container = document.querySelector(settings.container);
    if (!container) {
      console.error('CRSET Chat: Container não encontrado:', settings.container);
      return;
    }
    
    createWidget(container, settings);
  };
  
  function createWidget(container, settings) {
    const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const widgetHTML = `
      <div id="crset-chat-container" style="position: fixed; ${settings.position === 'bottom-right' ? 'bottom: 20px; right: 20px;' : 'bottom: 20px; left: 20px;'} z-index: 9999; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div id="crset-chat-button" style="width: 60px; height: 60px; background: linear-gradient(135deg, #2563eb, #1d4ed8); border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); transition: all 0.3s ease;">
          <svg width="24" height="24" fill="white" viewBox="0 0 24 24">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
          </svg>
        </div>
        <div id="crset-chat-window" style="display: none; width: 350px; height: 500px; background: white; border-radius: 12px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15); position: absolute; bottom: 80px; right: 0; overflow: hidden;">
          <div style="background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; padding: 16px; display: flex; justify-content: space-between; align-items: center;">
            <div>
              <h3 style="margin: 0; font-size: 16px; font-weight: 600;">CRSET AI Assistant</h3>
              <p style="margin: 0; font-size: 12px; opacity: 0.9;">Como posso ajudar?</p>
            </div>
            <button id="crset-chat-close" style="background: none; border: none; color: white; cursor: pointer; font-size: 20px; padding: 0; width: 24px; height: 24px;">×</button>
          </div>
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
              <p style="margin: 0; color: #475569; font-size: 14px; line-height: 1.5;">Olá! 👋 Sou o assistente da CRSET Solutions. Como posso ajudá-lo hoje?</p>
            </div>
          </div>
          <div style="padding: 16px; border-top: 1px solid #e2e8f0; background: white;">
            <div style="display: flex; gap: 8px;">
              <input id="crset-chat-input" type="text" placeholder="Digite sua mensagem..." style="flex: 1; padding: 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 14px; outline: none;">
              <button id="crset-chat-send" style="background: #2563eb; color: white; border: none; padding: 12px 16px; border-radius: 8px; cursor: pointer; font-size: 14px;">Enviar</button>
            </div>
          </div>
        </div>
      </div>
    `;
    
    container.innerHTML = widgetHTML;
    setupEventListeners(settings, sessionId);
  }
  
  function setupEventListeners(settings, sessionId) {
    const button = document.getElementById('crset-chat-button');
    const window = document.getElementById('crset-chat-window');
    const closeBtn = document.getElementById('crset-chat-close');
    const input = document.getElementById('crset-chat-input');
    const sendBtn = document.getElementById('crset-chat-send');
    const messages = document.getElementById('crset-chat-messages');
    
    button.addEventListener('click', () => {
      const isVisible = window.style.display !== 'none';
      window.style.display = isVisible ? 'none' : 'block';
      if (!isVisible) input.focus();
    });
    
    closeBtn.addEventListener('click', () => {
      window.style.display = 'none';
    });
    
    function sendMessage() {
      const message = input.value.trim();
      if (!message) return;
      
      addMessage('user', message);
      input.value = '';
      
      fetch(`${settings.apiUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message, session_id: sessionId })
      })
      .then(response => response.json())
      .then(data => {
        if (data.response) {
          addMessage('assistant', data.response);
        } else {
          addMessage('assistant', 'Desculpe, ocorreu um erro. Contacte-nos em info@crsetsolutions.com');
        }
      })
      .catch(error => {
        console.error('Erro na API:', error);
        addMessage('assistant', 'Estou temporariamente indisponível. Contacte info@crsetsolutions.com');
      });
    }
    
    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') sendMessage();
    });
    
    function addMessage(type, content) {
      const messageHTML = `
        <div style="background: white; padding: 12px; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
          <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="width: 24px; height: 24px; background: ${type === 'user' ? '#10b981' : '#2563eb'}; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 8px;">
              <svg width="12" height="12" fill="white" viewBox="0 0 24 24">
                ${type === 'user' 
                  ? '<path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>'
                  : '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>'
                }
              </svg>
            </div>
            <span style="font-weight: 600; color: #1e293b; font-size: 14px;">${type === 'user' ? 'Você' : 'CRSET Assistant'}</span>
          </div>
          <p style="margin: 0; color: #475569; font-size: 14px; line-height: 1.5;">${content}</p>
        </div>
      `;
      
      messages.insertAdjacentHTML('beforeend', messageHTML);
      messages.scrollTop = messages.scrollHeight;
    }
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('crset-chat-widget');
    if (container && !container.innerHTML.trim()) {
      window.CRSETChat.init();
    }
  });
  
})();
"""
    
    response = app.response_class(
        widget_content,
        mimetype='application/javascript',
        headers={
            'Content-Type': 'application/javascript; charset=utf-8',
            'Cache-Control': 'public, max-age=3600'
        }
    )
    return response

@app.route('/widget.js')
def serve_widget():
    return send_from_directory(app.static_folder, 'widget.js', mimetype='application/javascript')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
