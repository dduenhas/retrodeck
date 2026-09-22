# RETRODECK — Stereo Cassette Deck MT-F1000

Webapp de player de áudio com visual de **tape deck analógico** (inspirado no Pioneer CT-F1000).
Arquivo único, sem dependências: `index.html` (HTML + CSS + JS + Web Audio API + IndexedDB).

## Como rodar

- **Simples:** duplo clique em `index.html`.
- **Recomendado** (microfone, armazenamento, service worker/PWA):

```bash
cd E:\PROJETOS\mimo-proj
python serve.py 8080
# http://localhost:8080
```

> `serve.py` garante o MIME `text/javascript` para o `sw.js` — o `python -m http.server`
> padrão pode servir `.js` como `text/plain` em Windows, o que bloqueia o service worker.

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
- **CARREGAR PLAYLIST**: importa um .m3u8/.m3u/.json baixado; com o caminho por faixa no
  arquivo, tudo resolve pelo cache do navegador ou **vinculando a pasta uma única vez**.
- **Download .m3u8** de qualquer playlist salva, com o **caminho relativo do arquivo**.
- **Reordenação manual**: arraste as faixas com o mouse (no toque, pressione ~0,2 s e arraste).
- Botão **🔀 (símbolo universal de shuffle)** embaralha a lista na hora, mantendo a faixa
  atual selecionada.
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

## Ajuste de áudio

- Knob **BALANCE L·R** (ao lado de Volume/Mic Gain/Tone): ajuste fino do estéreo —
  `C` no centro, `L1..L10` / `R1..R10` para os lados. Persistido entre sessões.
- Switch **MONO**: ligado, converte a saída estéreo em mono ((L+R)/2) — resolve músicas
  desbalanceadas. Vale também para a gravação (fonte MIC+MUSIC).

## Tela cheia, PWA e segundo plano

- Botão **quadrado no header** (à direita de MT-F1000) alterna **tela cheia** (oculto em
  navegadores sem suporte).
- **PWA instalável**: `manifest.webmanifest` + service worker com cache offline do shell,
  ícone K7 próprio (PNG/SVG/ICO). Em HTTPS (GitHub Pages) o navegador oferece instalar.
- **Tocar com a tela fechada**: Media Session API com metadados/arte e ações
  (play, pause, próxima, anterior, busca) na tela de bloqueio; a reprodução **não é pausada**
  ao esconder a aba/aplicação e o áudio é retomado ao voltar.

## Segurança

- Aplicação 100% first-party: sem CDNs, fontes, scripts ou telemetria de terceiros.
- CSP restritiva no `<head>` (`default-src 'self'`, `object-src 'none'`, `base-uri 'self'`).
- Dados (áudios, playlists, configurações) ficam só no IndexedDB local — nada é enviado a
  servidor. O service worker só cacheia a mesma origem.

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
deck.loadPlaylistFile(File)    // carrega .m3u8/.m3u/.json como playlist
deck.shuffle()                 // embaralha a lista (mantém faixa atual)
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
