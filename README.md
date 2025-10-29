# 👋🏻 Leonardo de Moura Fuseti

Estudante de Defesa Cibernetica no Polo Estacio Piumhi MG . Formação tecnica em Tecnico em Redes de Computadores no IFMG Bambui MG , intusiasta na programação gostando muito de Python e evoluindo dia a dia .

### Conecte-se comigo

[![Perfil DIO](https://img.shields.io/badge/-Meu%20Perfil%20na%20DIO-30A3DC?style=for-the-badge)](https://www.dio.me/users/mourafuseti)
[![E-mail](https://img.shields.io/badge/-Email-000?style=for-the-badge&logo=microsoft-outlook&logoColor=E94D5F)](mailto:mourafuseti@gmail.com)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-000?style=for-the-badge&logo=linkedin&logoColor=30A3DC)](https://www.linkedin.com/in/leonardo-moura-fuseti-4052b0359/)

### Habilidades

![HTML](https://img.shields.io/badge/HTML-000?style=for-the-badge&logo=html5&logoColor=30A3DC)
![CSS3](https://img.shields.io/badge/CSS3-000?style=for-the-badge&logo=css3&logoColor=E94D5F)
![JavaScript](https://img.shields.io/badge/JavaScript-000?style=for-the-badge&logo=javascript&logoColor=F0DB4F)
![Sass](https://img.shields.io/badge/SASS-000?style=for-the-badge&logo=sass&logoColor=CD6799)
![Bootstrap](https://img.shields.io/badge/bootstrap-000?style=for-the-badge&logo=bootstrap&logoColor=553C7B)
[![Git](https://img.shields.io/badge/Git-000?style=for-the-badge&logo=git&logoColor=E94D5F)](https://git-scm.com/doc)
[![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=30A3DC)](https://docs.github.com/)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

### GitHub Stats

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=mourafuseti&theme=transparent&bg_color=000&border_color=30A3DC&show_icons=true&icon_color=30A3DC&title_color=E94D5F&text_color=FFF)

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-Custom-red)
![Version](https://img.shields.io/badge/version-8.1-green)
```markdown
# WiFi Auditor Pro v8.1



> **Ferramenta de Pentest Automatizado com Interface Interativa para Auditoria de Redes Wi-Fi (WPA/WPA2/WPS)**  
> **Desenvolvido por Leonardo de Moura Fuseti**  
> **Copyright © 2025 - Todos os Direitos Reservados**

---

## ⚠️ **AVISO LEGAL**

> **Esta ferramenta é destinada exclusivamente para uso em redes Wi-Fi que você possui ou tem autorização explícita para testar.**  
> O uso não autorizado viola leis de acesso a redes e privacidade (ex: Lei Geral de Proteção de Dados - LGPD no Brasil, Computer Misuse Act, etc).  
> **O desenvolvedor não se responsabiliza por uso indevido.**

---

## 🚀 Funcionalidades

| Módulo | Descrição |
|-------|----------|
| **Handshake WPA/WPA2** | Captura handshake com `airodump-ng` + `aireplay-ng` e quebra com `aircrack-ng` |
| **Ataque em Massa** | Ataca múltiplas redes automaticamente |
| **Wordlist Personalizável** | Suporte a `rockyou.txt`, arquivos customizados ou download automático |
| **Interface em Monitor** | Ativa modo monitor com `airmon-ng` |
| **Relatórios Automáticos** | Salva senhas encontradas e histórico em `/home/kali/wifi_auditor_pro` |
| **Interface Colorida** | Menu interativo com cores e progresso em tempo real |
| **Limpeza Automática** | Finaliza processos e interfaces ao encerrar (`Ctrl+C`) |

---

## 📁 Estrutura de Saída

Todos os arquivos são salvos em:

```
/home/kali/wifi_auditor_pro/
├── NOME_REDE_XX:XX:XX.cap        → Handshake capturado
├── nome_personalizado.txt        → Senha encontrada (com dados)
└── relatorio.txt                 → Log de todos os ataques
```

---

## ⚙️ Requisitos

- **Sistema Operacional**: Kali Linux (recomendado)
- **Permissões**: `root` (sudo)
- **Ferramentas necessárias**:

```bash
sudo apt update && sudo apt install -y \
    aircrack-ng \
    airmon-ng \
    airodump-ng \
    aireplay-ng \
    iwconfig \
    wget \
    gunzip
```

---

## 📥 Instalação

1. **Clone ou baixe o script**:

```bash
wget https://github.com/mourafuseti/wifi_auditor_pro/wifi_auditor_pro.py
# ou copie o código para um arquivo
```

2. **Dê permissão de execução**:

```bash
chmod +x wifi_auditor_pro.py
```

3. **Execute com sudo**:

```bash
sudo python3 wifi_auditor_pro.py
```

---

## 🎮 Como Usar

### Passo a Passo

1. **Inicie o programa**
2. **Configure a interface Wi-Fi** (ex: `wlan0` → será convertida para modo monitor)
3. **Escolha a wordlist** (recomendado: `rockyou.txt`)
4. **Inicie os ataques**:
   - `1` → Scan + Handshake (melhor opção)
   - Escolha uma rede ou `0` para ataque em massa
5. **Aguarde captura e quebra da senha**
6. **Salve com nome personalizado**
7. **Consulte relatórios em `5`**

---

## 🔧 Comandos Internos (Resumo)

| Ação | Comando Interno |
|------|-----------------|
| Modo Monitor | `airmon-ng start wlan0` |
| Scan | `airodump-ng wlan0mon -w /tmp/scan_... --output-format csv` |
| Deauth | `aireplay-ng --deauth 7 -a BSSID wlan0mon` |
| Captura | `airodump-ng -c CH --bssid BSSID -w /tmp/hs_... wlan0mon` |
| Quebra | `aircrack-ng -w wordlist -b BSSID arquivo.cap -l keyfile` |

---

## 📊 Exemplo de Arquivo de Senha Salvo

```txt
REDE: MinhaRede
BSSID: AA:BB:CC:DD:EE:FF
SENHA: MinhaSenha123
TEMPO: 245s
TESTADAS: 1,234,567
DATA: 2025-04-05 14:32:10
```

---

## 🛠️ Desenvolvimento & Contribuição

- Código aberto para fins **educacionais**
- Contribuições via Pull Request são bem-vindas
- Reporte bugs por e-mail ou issues

---

## 📧 Contato

**Desenvolvedor**: Leonardo de Moura Fuseti  
**Ano**: 2025  
**Uso**: Apenas em ambientes autorizados

---

> **"Conhecimento é poder. Use com responsabilidade."**
```



Agora seu projeto tem uma documentação profissional, clara e segura! 🔒
```
