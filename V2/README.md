# MIMO PROJ — Stereo Cassette Deck MT-F1000

Webapp de player de áudio com visual de **tape deck analógico** (inspirado no Pioneer CT-F1000).
Arquivo único, sem dependências: `index.html` (HTML + CSS + JS + Web Audio API + IndexedDB).

## Como rodar

- **Simples:** duplo clique em `index.html`.
- **Recomendado** (garante microfone + armazenamento estável):

```bash
cd E:\PROJETOS\mimo-proj
python -m http.server 8080
# http://localhost:8080
```

## Transporte e indicadores

- **PLAY · PAUSE · STOP · REW · F.FWD · REC** com curso físico ao pressionar.
- Segurar REW/F.FWD = shuttle analógico (~14x). Toque rápido: REW = início da fita,
  F.FWD = próxima faixa.
- **Switch AFTER SHUTTLE**: `RESUME` (padrão) — ao soltar o shuttle a música **continua
  tocando do ponto**; `HOLD` — fica pausada e você aperta PLAY.
- LEDs: POWER, PLAY, REW, F.FWD, REC, PEAK +3dB, LOOP — cada um acende conforme a ação.
- **VUs analógicos estéreo** com balística real (ataque rápido / release lento), zona
  vermelha 0…+3 dB, arco de % de modulação e LED de PEAK com hold.
- **VU dedicado MIC INPUT** no painel de gravação: mostra a captação do microfone
  enquanto grava (STANDBY fora da gravação).
- Janela de fita animada: carretéis com velocidade linear constante (o pacote de fita
  muda de raio com o progresso), 3 cabeças, capstan, contador mecânico de 3 dígitos.
- **Nomes longos**: o título da fita faz **marquee** no LCD e na label da fita, sem
  quebrar o layout.

## Playlist (Program Play)

- Abra vários arquivos de uma vez (mp3, wav, ogg, m4a, flac…) — botão ou arraste-e-solte.
- Clique numa faixa para tocar; avanço automático no fim; switch LOOP.
- Botão **✕** remove a faixa; **CLEAR** limpa tudo (com confirmação).
- **Persistência automática no IndexedDB do navegador**: feche e reabra o navegador que
  a playlist, as gravações e as configurações voltam (arquivos guardados como blobs).
- **SALVAR PLAYLIST**: guarde até **10 playlists nomeadas** (▶ abrir, ⬇ baixar, ✕ excluir).
- **Download .m3u8** de qualquer playlist salva (formato padrão).
- **Importar .m3u8/.json** pelo próprio ADD FILES: faixas não localizadas aparecem em
  **vermelho** com botão **LOCALIZAR** para reapontar o arquivo que mudou de lugar.

## Gravação (Mic Recording)

- Botão REC (ou o vermelho do transporte): grava o microfone do navegador, **com
  música de fundo** (switch RECORD SOURCE: `MIC+MUSIC`) **ou só o microfone** (`MIC ONLY`).
- Switch **MONITOR** ouve o microfone pelos alto-falantes enquanto grava.
- Cada take entra na lista e na playlist (badge **REC**), com:
  - **✎ renomear** (ou duplo clique no nome)
  - **⬇ baixar** o arquivo .webm
  - **✕ excluir**
- **LIMPAR GRAVAÇÕES** remove todos os takes (com confirmação).

## Atalhos

| Tecla   | Ação                          |
|---------|-------------------------------|
| Espaço  | Play / Pause                  |
| S       | Stop                          |
| ← / →   | Shuttle REW / F.FWD (segure)  |

## API pública (automação/testes)

```js
deck.addFiles(FileList)        // arquivos de áudio e/ou .m3u8/.json
deck.play() / pause() / stop()
deck.shuttle(-1|1) / shuttleRelease()
deck.rec() / stopRec()
deck.locate(idx, autoplay)     // localizar faixa ausente
deck.savePlaylist()            // usa o formulário aberto
deck.loadSaved(id, skipConfirm)
deck.toM3u(tracks, nome)       // gera o conteúdo .m3u8
deck.vu / deck.micVu           // níveis em dB
deck.state / deck.storageOK
```

## Estrutura de dados (IndexedDB `mimo-deck-v1`)

| Store    | Conteúdo                                              |
|----------|-------------------------------------------------------|
| `files`  | blobs de áudio (playlist atual + takes), chave = nome |
| `kv`     | ordem da playlist, faixa atual, configurações         |
| `plists` | playlists salvas (máx. 10), manifestos com nome/dur   |

Arquivos não referenciados pela playlist atual nem por playlists salvas são removidos
automatically para não encher o disco (os originais continuam no seu computador).
