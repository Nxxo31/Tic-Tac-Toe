# triqui — Contexto del agente

## Proyecto
Tres en raya (Tic-Tac-Toe) PWA con modos de dificultad, leaderboard y animaciones. V2 activa.

## Stack
- Vanilla HTML + CSS + JS (sin frameworks)
- PWA: manifest.json + sw.js
- Deploy: Vercel (vercel.json presente)

## Archivos clave
- index.html — app completa
- sw.js — service worker
- manifest.json — PWA config

## Reglas críticas
- Sin dependencias npm — vanilla puro
- Cambios en sw.js → incrementar CACHE_VERSION

## Loop de trabajo
1. Editar index.html / sw.js
2. Probar en browser
3. Commit atómico en español → push
