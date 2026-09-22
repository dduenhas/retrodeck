# MIMO PROJ — Stereo Cassette Deck MT-F1000

Webapp de player de áudio com visual de **tape deck analógico** (inspirado no Pioneer CT-F1000).

## Como rodar

Abrir direto no navegador (duplo clique em `index.html`), ou servir localmente:

```bash
cd E:\PROJETOS\mimo-proj
python -m http.server 8080
# http://localhost:8080
```

> Gravação por microfone exige contexto seguro: `http://localhost` ou HTTPS.
> (Em `file://` o Chrome costuma permitir, mas localhost é garantido.)

## Recursos

- **Transporte**: PLAY, PAUSE, STOP, REW, F.FWD (segure REW/FF = shuttle analógico;
  toque REW = início da fita, toque FF = próxima faixa), REC.
- **LEDs**: POWER, PLAY, REW, F.FWD, REC, PEAK +3dB, LOOP — acendem conforme a ação.
- **VU analógicos estéreo** (L/R) com balística real: ataque rápido, release lento,
  zona vermelha 0…+3 dB e LED de PEAK.
- **Janela de fita animada**: carretéis com velocidade linear constante (raio do pacote
  de fita muda com o progresso), cabeças, capstan, label com o nome da faixa.
- **Playlist**: abra vários arquivos (mp3, wav, ogg, m4a, flac…), clique para tocar,
  avanço automático, loop, arraste-e-solte em qualquer lugar da página.
- **Gravação por microfone** (MediaRecorder): com música de fundo (`MIC + MUSIC`)
  ou só o microfone (`MIC ONLY`), monitoração opcional. Cada take entra na playlist
  e tem link de download.
- **Controles**: knobs de VOLUME, MIC GAIN e TONE (arraste vertical), switches de
  fonte de gravação, monitor e loop, contador mecânico de 3 dígitos + display LCD.

## Atalhos

| Tecla   | Ação                    |
|---------|-------------------------|
| Espaço  | Play / Pause            |
| S       | Stop                    |
| ← / →   | Shuttle REW / F.FWD (segure) |

## API pública (automação/testes)

```js
deck.addFiles(FileList)   // adiciona à playlist
deck.play() / deck.pause() / deck.stop()
deck.shuttle(-1|1) / deck.shuttleRelease()
deck.rec() / deck.stopRec()
deck.vu                    // [L, R] em dB
deck.state                 // estado completo
```

## Estrutura

Arquivo único: `index.html` (HTML + CSS + JS, sem dependências, usa Web Audio API).
