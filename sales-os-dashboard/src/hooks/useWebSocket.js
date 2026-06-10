import { useEffect, useRef, useState } from 'react';

export default function useWebSocket(url) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const wsRef = useRef(null);
  const handlersRef = useRef(new Set());

  useEffect(() => {
    if (!url) return;
    let reconnectTimer;

    const connect = () => {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => setIsConnected(true);
      ws.onclose = () => {
        setIsConnected(false);
        reconnectTimer = setTimeout(connect, 3000);
      };
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setLastMessage(data);
          handlersRef.current.forEach(fn => fn(data));
        } catch { /* ignore parse errors */ }
      };
      ws.onerror = () => ws.close();
    };

    connect();
    return () => {
      clearTimeout(reconnectTimer);
      wsRef.current?.close();
    };
  }, [url]);

  const subscribe = (handler) => {
    handlersRef.current.add(handler);
    return () => handlersRef.current.delete(handler);
  };

  return { isConnected, lastMessage, subscribe };
}
