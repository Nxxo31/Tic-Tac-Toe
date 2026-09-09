## PROJECT.md — Fuente de Verdad (OBLIGATORIO)
PROJECT.md es la **unica fuente de verdad** del estado, desarrollo y documentacion de este proyecto.
- Leer PROJECT.md ANTES de cualquier accion.
- Actualizar PROJECT.md DESPUES de cada desarrollo significativo.
- No crear .md separados para specs, docs o arquitectura — todo va en PROJECT.md.

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
