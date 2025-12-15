import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Pizza } from 'phosphor-react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Olá! Bem-vindo à Pizza Bot. Gostaria de ver o cardápio ou fazer um pedido?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/chat', {
        message: userMessage.text,
        thread_id: "user-123"
      });

      const botMessage = { sender: 'bot', text: response.data.response };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages(prev => [...prev, { sender: 'bot', text: 'Desculpe, ocorreu um erro ao processar sua mensagem.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <Pizza size={32} />
        <h1>Pizza Bot</h1>
      </header>
      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              <div className="message-content">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.text}</ReactMarkdown>
              </div>
            </div>
          ))}
          {loading && <div className="message bot"><div className="message-content">Digitando...</div></div>}
          <div ref={messagesEndRef} />
        </div>
        <div className="input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Digite sua mensagem..."
            disabled={loading}
          />
          <button onClick={sendMessage} disabled={loading}>Enviar</button>
        </div>
      </div>
    </div>
  );
}

export default App;
