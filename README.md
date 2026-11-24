# Google AI Pro / Ultra — Guia Atualizado (2026-11)

Guia prático e funcional para consultar e ativar trials do Google AI Pro / AI Ultra
usando um emulador Android com root + Frida, explorando o **Google Play BillingClient**
da mesma forma que o app Google One faz.

> **Status do método em Nov/2026:** o cupom `US$19,99/3 meses` do AI Ultra
> (`g1.ai.ultra.3months_ip_90p.acq`) **não existe mais** no catálogo do Google.
> O que ainda funciona é o **trial grátis de 12 / 6 / 3 meses do Google AI Pro (5 TB)**.

---

## Sumário

1. [O que mudou desde o tutorial original](#o-que-mudou)
2. [Requisitos](#requisitos)
3. [Instalação passo a passo](#instalação)
4. [Como o script funciona](#como-funciona)
5. [Uso](#uso)
6. [Os offers disponíveis hoje](#offers-disponíveis)
7. [Correções aplicadas](#correções-aplicadas)
8. [Solução de problemas](#solução-de-problemas)
9. [Avisos](#avisos)

---

## O que mudou

O tutorial original (Google AI Ultra 30TB por US$19,99/mês) usava o SKU:

```
g1.ai.ultra.3months_ip_90p.acq
```

**Esse SKU foi removido pelo Google.** Ao consultar o BillingClient em Nov/2026,
ele não retorna mais nenhum offer. O AI Ultra só aparece com preço cheio.

O que **ainda está disponível** são os trials do **Google AI Pro (5 TB)**:

| Offer ID | Produto | Preço | Período |
|----------|---------|-------|---------|
| `12months-eft` | Google AI Pro (5 TB) | **GRÁTIS** | 12 meses |
| `6months-eft` | Google AI Pro (5 TB) | GRÁTIS | 6 meses |
| `6months-eft-2` | Google AI Pro (5 TB) | GRÁTIS | 6 meses |
| `6months-eft-ss-2026` | Google AI Pro (5 TB) | GRÁTIS | 6 meses |
| `eft-3mo` | Google AI Pro (5 TB) | GRÁTIS | 3 meses |

Após o trial, o preço normal do AI Pro é ~US$96,99/mês.

---

## Requisitos

### PC (Windows)
- Python 3.9+ (testado com 3.14)
- Frida **16.5.9** — obrigatório. Frida 17.x **não funciona** (removeu o Java bridge)
- ADB (Android platform-tools) no PATH

### Emulador
- **MuMu Player** com Android 12 (testado em `SM-A5560`)
- Root ativado (`adb root` funciona, `uid=0`)
- ADB debugging ativado nas configurações do MuMu
- Play Store + Google Play Services instalados e funcionando
- Conta Google logada (de preferência uma conta secundária)

---

## Instalação

### 1. Python e Frida

```powershell
python -m pip install "frida==16.5.9"
python -c "import frida; print(frida.__version__)"   # deve imprimir 16.5.9
```

### 2. MuMu Player

1. Baixe em https://www.mumu.com/
2. Instale e crie uma imagem **Android 12**
3. Em **Configurações → Root**, ative "ROOT permissions"
4. Em **Configurações → Opções do desenvolvedor**, ative "USB debugging"
5. Reinicie o emulador
6. Abra a Play Store, faça login e **adicione um cartão de crédito**
   (obrigatório mesmo para trials grátis)

### 3. Conectar o ADB

O MuMu normalmente usa a porta **7555** (ou 16416):

```powershell
adb connect 127.0.0.1:7555
adb -s 127.0.0.1:7555 root
adb -s 127.0.0.1:7555 shell id       # deve mostrar uid=0(root)
```

Para descobrir a porta do seu MuMu:

```powershell
adb connect 127.0.0.1:16384
adb connect 127.0.0.1:7555
adb connect 127.0.0.1:16416
adb connect 127.0.0.1:62001
adb connect 127.0.0.1:21503
adb devices
```

O modelo do MuMu aparece como `SM-A5560`. O emulador do Android Studio
aparece como `sdk_gphone64_x86_64` (`emulator-5554`/`5556`) — **não use ele**.

---

## Como o funciona

O script `ultra0.py`:

1. Conecta via ADB, verifica root
2. Inicia o `frida-server` no dispositivo (baixa a versão correta se necessário)
3. Empurra um módulo de billing (`module_521.apk`) para `/data/local/tmp/`
4. Garante que o processo da Play Store (`com.android.vending`) está rodando
5. Inicia o **Google One** e injetaFrida nele
6. Usa `DexClassLoader` para carregar o módulo de billing
7. Chama `BillingClient.queryProductDetailsAsync` para vários product IDs
8. Lê os offers retornados (offerId, preço em micros, período, token)
9. Com `--allow-paid`, permite offers pagos; sem isso, só aceita preço 0
10. Chama `launchBillingFlow` na main thread para abrir o checkout
11. Verifica o preço na tela antes de confirmar (proteção)

Nada é enviado para servidores externos — tudo roda localmente.

---

## Uso

### Modo seguro — apenas listar offers (zero risco)

```powershell
python ultra0.py --list --no-add --force --serial 127.0.0.1:7555
```

### Ativar trial de 12 meses do AI Pro (o melhor)

```powershell
python ultra0.py --account "current@device" --no-add --force --plan pro12 --serial 127.0.0.1:7555
```

### Ativar trial de 6 meses

```powershell
python ultra0.py --account "current@device" --no-add --force --plan pro6 --serial 127.0.0.1:7555
```

### Ativar trial de 3 meses

```powershell
python ultra0.py --account "current@device" --no-add --force --plan pro3 --serial 127.0.0.1:7555
```

### Adicionar uma conta nova ao dispositivo

```powershell
python ultra0.py --account "email:senha:" --force --serial 127.0.0.1:7555
```

(se a conta já estiver no dispositivo, use `--no-add`)

### Flags importantes

| Flag | Uso |
|------|-----|
| `--list` | Só consulta offers, não clica em nada |
| `--no-add` | Não tenta adicionar a conta (use quando já está logada) |
| `--force` | Pula a verificação da conta do Play (necessário no MuMu, onde a UI não é legível via uiautomator) |
| `--plan pro12 / pro6 / pro3` | Escolhe qual trial do AI Pro ativar |
| `--allow-paid` | Permite offers pagos (não use para trials) |
| `--sku <id>` | Força um product ID específico |
| `--serial <porta>` | Especifica a porta ADB do MuMu |

---

## Offers disponíveis

Valores em micros divididos por 1.000.000 = preço real:

- `779900000` → US$779,90 — AI Ultra 20TB (preço cheio)
- `999900000` → US$999,90 — AI Ultra 30TB (preço cheio)
- `96990000` → US$96,99 — AI Pro 5TB (preço cheio)
- `49990000` → US$49,99 — AI Plus 2TB (preço cheio)
- `0` → **GRÁTIS** (offers `12months-eft`, `6months-eft`, `eft-3mo`)

---

## Correções aplicadas

Este repositório contém duas correções importantes aplicadas ao `ultra0.py` original:

### 1. UTF-8 no stdout
O script original usa `✅` e caracteres chineses nos `print()`. No Windows (cp1252)
isso gera `UnicodeEncodeError`. Correção:

```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

### 2. Reconhecimento de português
A função `confirm_zero()` original só reconhecia "Subscribe"/"订阅".
No MuMu em português aparece "**Assinar**" e "R$". Correção aplicada em
`ultra0_pt.py`:

- Detecta "Assinar" como botão de confirmação
- Reconhece "R$" no regex de preço
- Reconhece "grátis"/"gratis" como preço zero
- **Não clica automaticamente** — deixa a finalização na sua mão

---

## Stack de trial (acumular até 24 meses)

O Google permite **upgrade de assinatura** usando o `purchaseToken` da assinatura
atual com `ReplaceProrationMode = 5` (`CHARGE_FULL_PRICE`). Isso faz o Google
"dobrar" o tempo restante. Sequência validada:

| Passo | Plan | Offer | Tempo total |
|-------|------|-------|-------------|
| 1 | `pro12` | `12months-eft` | 12 meses |
| 2 | `--stack --plan pro6` | `6months-eft` | 18 meses |
| 3 | `--stack --plan pro6b` | `6months-eft-2` | 24 meses |
| 4 | `--stack --plan pro6c` | `6months-eft-ss-2026` | ❌ **QUEBRADO** |

### ⚠️ Teto real: 24 meses

O **Passo 4** (`6months-eft-ss-2026`) falha sempre com "Ocorreu um erro do nosso lado.
Tente novamente." — testado em múltiplas contas e emuladores diferentes. O offer
é listado no BillingClient mas recusado no checkout. **Não adianta insistir.**

### Comandos (use `ultra0_stack.py`)

```powershell
# Passo 1 — 12 meses
python ultra0_stack.py --account "current@device" --no-add --force --plan pro12 --serial 127.0.0.1:16384

# Passo 2 — +6 (18 meses)
python ultra0_stack.py --account "current@device" --no-add --force --stack --plan pro6 --serial 127.0.0.1:16384

# Passo 3 — +6 (24 meses)
python ultra0_stack.py --account "current@device" --no-add --force --stack --plan pro6b --serial 127.0.0.1:16384
```

Ou pelos launchers em `scripts/`:
```powershell
python scripts/run_stack_step1.py
python scripts/run_stack_step2.py
python scripts/run_stack_step3.py
```

### Dicas que funcionaram

- **Reinicie o emulador antes de cada stack.** O Play Store entra em estado
  degradado ("failed to attach") depois de várias execuções — um restart limpo
  resolve.
- O script lê o `purchaseToken` automaticamente do `library.db`
  (`/data/data/com.android.vending/databases/library.db`).
- Entre passos, aguarde alguns segundos para o DB gravar o novo token.
- Use `scripts/check_validity2.py` para conferir a data de validade após cada passo.

### Diferenças do `ultra0_stack.py`

Este arquivo é o `ultra0.py` com:
- `getActivity()` corrigido (usa `mActivities` em vez de `Java.choose`, que falha
  em Android 12 x86_64)
- UTF-8 no stdout
- Suporte a português ("Assinar", "R$", "grátis") sem clicar automaticamente

---

## Solução de problemas

### "Play Store não inicia / failed to attach - start timeout"
Reinicie o MuMu. Se persistir, limpe o cache:
```
adb -s 127.0.0.1:7555 shell pm clear com.android.vending
```

### "Root não detectado"
```
adb -s 127.0.0.1:7555 root
```
Se não funcionar, ative root nas configurações do MuMu e reinicie.

### "Play account switch failed / current account unknown"
Use `--force` para pular a verificação (o MuMu não deixa a UI ser lida via uiautomator).

### "Nenhum dispositivo encontrado"
Conecte na porta correta (veja seção [Conectar o ADB](#3-conectar-o-adb)).

### "Oferta não aparece"
Cada conta Google tem direito a **um trial apenas**. Se você já iniciou um trial
(mesmo sem confirmar), a oferta desaparece. Use outra conta.

### "Módulo não encontrado"
O script empurra o módulo automaticamente na primeira execução.

---

## Avisos

- ⚠️ Use contas **secundárias**. Nunca use sua conta principal.
- ⚠️ Cada conta tem **uma chance** de trial. Uma vez iniciado, não volta.
- ⚠️ **Sempre confira o preço na tela** antes de confirmar qualquer pagamento.
- ⚠️ O script não automaticamente confirma pagamentos com valor > 0.
- ⚠️ Trials grátis ainda cobram after o período se você não cancelar.
  Vá em `Play Store → Avatar → Pagamentos e assinaturas → Assinaturas`
  para cancelar antes do vencimento.
- ⚠️ Isto explora um comportamento do **cliente** (Play BillingClient).
  Não modifica dados do servidor do Google. Use por sua conta e risco.

---

## Estrutura do repositório

```
.
├── README.md              # este guia
├── GUIA_RAPIDO.md         # resumo de uma página
├── ultra0.py              # script original (com correção UTF-8)
├── ultra0_pt.py           # script com suporte a português + não-clique
├── setup_env.py           # setup automático de ambiente
├── query_sku.py           # utilitário de consulta de SKU
├── requirements.txt       # frida>=16.0
├── ultra0_stack.py        # versão stack (getActivity corrigido + PT)
├── scripts/
│   ├── launch_check.ps1      # verificação de ambiente
│   ├── launch_list.ps1       # listar offers
│   ├── launch_trial.ps1      # ativar trial
│   ├── run_stack_step1.py    # stack: 12 meses
│   ├── run_stack_step2.py    # stack: +6 (18 meses)
│   ├── run_stack_step3.py    # stack: +6 (24 meses)
│   ├── run_stack_step4.py    # stack: +6 (quebrado, documentado)
│   ├── run_pro3.py           # trial 3 meses
│   ├── run_pro6.py           # trial 6 meses
│   ├── check_validity2.py    # conferir validade no library.db
│   ├── resumo_contas.py      # resumir assinaturas por conta
│   └── check_all_offers_new.py # listar todas as offers
└── accounts.example.txt   # exemplo de formato de conta
```
