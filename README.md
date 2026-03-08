# 🛠️ Canivete TI PRO - Suporte N2/N3

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

O **Canivete TI PRO** é uma ferramenta de automação desenvolvida para técnicos de suporte e analistas de infraestrutura. O objetivo é centralizar e agilizar diagnósticos complexos de rede, reparação de sistema e limpeza de ativos, reduzindo o tempo de atendimento em chamados de nível 2 e 3.

---

## 🚀 Principais Funcionalidades

### 🌐 Diagnóstico de Rede (Foco em Provedores)
- **Auto Fix Internet:** Reset completo da pilha TCP/IP, Winsock e renovação de DHCP em um clique.
- **Diagnóstico Completo:** Varredura automática (Ping, Tracert, NSLookup, Tabela ARP e Rotas) com exportação direta para `.txt` com carimbo de tempo (timestamp).
- **Análise de Portas:** Identificação de conexões ativas e PIDs de processos.

### 🧰 Manutenção do Sistema
- **Reparação Nativa:** Atalhos configurados para `SFC Scannow`, `DISM` e `Chkdsk`.
- **Gestão de Serviços:** Acesso rápido ao `services.msc`, `regedit` e `msconfig`.
- **Limpeza Profunda:** Remoção de temporários de usuário e sistema, além de esvaziamento forçado de lixeira.

### 🐧 Versão Linux (Bash Scripts)
- Gestão de Firewall com `UFW`.
- Limpeza de pacotes órfãos e cache `APT`.
- Análise de logs críticos via `Journalctl`.

---

## 📦 Como Executar

### Windows
1. Baixe o executável na pasta `dist` ou o script `.py`.
2. **Importante:** Clique com o botão direito e selecione **Executar como Administrador**.
3. Requisitos: Windows 10 ou 11.

### Linux
1. Certifique-se de ter o Python 3 e o CustomTkinter instalados:
   ```bash
   pip3 install customtkinter


   ````
   Execute com privilégios de Superusuário:

   ```bash
   sudo python3 CaniveteLinux.py

   ````
   🛠️ Tecnologias Utilizadas
Linguagem: Python 3.x

Interface Gráfica: CustomTkinter (Modern Dark UI)

Bibliotecas: subprocess, threading, wmi, psutil.


👨‍💻 Desenvolvedor
Matheus Huank Analista de Sistemas.
