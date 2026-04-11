import { useEffect, useRef } from 'react';
import { useAppSelector } from '@/hooks/storeHooks';

const WS_URL = import.meta.env.VITE_WS_URL;
const API_URL = import.meta.env.VITE_API_URL;
const PING_INTERVAL_MS = 25000;

const fetchWsTicket = async (): Promise<string | null> => {
	try {
		const res = await fetch(`${API_URL}/auth/ws-ticket`, { credentials: 'include' });
		if (!res.ok) return null;
		const data = await res.json();
		return data.ticket as string;
	} catch {
		return null;
	}
};

export const useNotificationsWS = (onMessage?: (message: string) => void) => {
	const isAuthenticated = useAppSelector((state) => state.auth.isAuthenticated);
	const wsRef = useRef<WebSocket | null>(null);
	const pingRef = useRef<ReturnType<typeof setInterval> | null>(null);
	const reconnectRef = useRef<ReturnType<typeof setTimeout> | null>(null);
	const isMountedRef = useRef(true);

	useEffect(() => {
		isMountedRef.current = true;

		if (!isAuthenticated) return;

		const connect = async () => {
			if (!isMountedRef.current) return;

			const ticket = await fetchWsTicket();
			if (!ticket || !isMountedRef.current) return;

			const ws = new WebSocket(`${WS_URL}/${ticket}`);
			wsRef.current = ws;

			ws.onopen = () => {
				pingRef.current = setInterval(() => {
					if (ws.readyState === WebSocket.OPEN) {
						ws.send('ping');
					}
				}, PING_INTERVAL_MS);
			};

			ws.onmessage = (event) => {
				onMessage?.(event.data);
			};

			ws.onclose = () => {
				if (pingRef.current) clearInterval(pingRef.current);
				if (isMountedRef.current) {
					reconnectRef.current = setTimeout(connect, 5000);
				}
			};

			ws.onerror = () => {
				ws.close();
			};
		};

		connect();

		return () => {
			isMountedRef.current = false;
			if (pingRef.current) clearInterval(pingRef.current);
			if (reconnectRef.current) clearTimeout(reconnectRef.current);
			wsRef.current?.close();
		};
	}, [isAuthenticated]);
};
