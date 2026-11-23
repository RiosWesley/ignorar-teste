# Guia Rápido — Google AI Pro Trial (Nov/2026)

## O que funciona hoje

✅ **Trial grátis de 12 meses do Google AI Pro (5TB)** — o melhor
⚠️ O cupom Ultra US$19,99/3 meses **não existe mais**

## 3 comandos

### 1. Instalar
```powershell
python -m pip install "frida==16.5.9"
```

### 2. Conectar MuMu (Android 12 + root)
```powershell
adb connect 127.0.0.1:7555
adb -s 127.0.0.1:7555 root
```

### 3. Listar offers (seguro)
```powershell
python ultra0.py --list --no-add --force --serial 127.0.0.1:7555
```

### 4. Ativar 12 meses grátis
```powershell
python ultra0_pt.py --account "current@device" --no-add --force --plan pro12 --serial 127.0.0.1:7555
```

A tela de pagamento abre. **Você finaliza manualmente.**

## Flags que importam

- `--list` → só consulta, não clica
- `--no-add` → conta já está no dispositivo
- `--force` → pula verificação da conta do Play (necessário no MuMu)
- `--plan pro12|pro6|pro3` → qual trial ativar

## Offers

| Nome | Preço |
|------|-------|
| 12months-eft | GRÁTIS 12 meses |
| 6months-eft | GRÁTIS 6 meses |
| eft-3mo | GRÁTIS 3 meses |
| null (AI Pro) | US$96,99/mês |
| null (AI Ultra 30TB) | US$999,90/mês |

## Cuidados

- Conta secundária apenas
- Uma chance de trial por conta
- Confira o preço antes de pagar
- Cancele antes do trial acabar
