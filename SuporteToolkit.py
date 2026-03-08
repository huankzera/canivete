import customtkinter as ctk
from tkinter import Text, END, Scrollbar, messagebox
import subprocess
import threading
import os
from datetime import datetime
import wmi
import psutil
import ctypes
import sys

class SuporteToolkit(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("CANIVETE TI PRO v1.0")
        self.geometry("1300x850")
        self.minsize(1150, 750)

        self.log_path = os.path.join(os.path.dirname(sys.executable), "suporte_log.txt")

        self.verificar_admin()
        self.configurar_interface()

    def verificar_admin(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            messagebox.showwarning(
                "Aviso Importante",
                "Execute o Canivete TI Pro como Administrador\npara que os comandos de reparação e limpeza funcionem!"
            )

    def configurar_interface(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==================== SIDEBAR (AÇÕES RÁPIDAS) ====================
        sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(sidebar, text="CANIVETE TI PRO", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(30, 5))
        # CORRIGIDO: text_color fora do CTkFont
        ctk.CTkLabel(sidebar, text="v1.0 - Nível Técnico", text_color="gray", font=ctk.CTkFont(size=12)).pack(pady=(0, 30))

        # Botões Mágicos (Auto Fix e Relatórios)
        ctk.CTkButton(sidebar, text="⚡ AUTO FIX INTERNET", fg_color="#b8860b", hover_color="#8a6508", font=ctk.CTkFont(weight="bold"),
                      command=self.auto_fix_internet).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(sidebar, text="🔎 Diagnóstico Completo (TXT)", fg_color="#1f538d", hover_color="#14375e", 
                      command=self.diagnostico_completo).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(sidebar, text="📋 Relatório de Hardware", fg_color="#1f538d", hover_color="#14375e", 
                      command=self.gerar_relatorio_wmi).pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(sidebar, text="🧹 Limpar Terminal", fg_color="#c42b1c", hover_color="#8a1f14", 
                      command=self.limpar_tela).pack(pady=10, padx=20, fill="x")

        # Comando Manual
        ctk.CTkLabel(sidebar, text="Comando Manual:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 5), padx=20, anchor="w")
        self.entry_comando = ctk.CTkEntry(sidebar, placeholder_text="Ex: ping 1.1.1.1")
        self.entry_comando.pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(sidebar, text="Executar", fg_color="green", hover_color="darkgreen", 
                      command=self.comando_manual).pack(pady=5, padx=20, fill="x")

        # Assinatura
        frame_assinatura = ctk.CTkFrame(sidebar, fg_color="transparent")
        frame_assinatura.pack(side="bottom", fill="x", pady=20)
        # CORRIGIDO: text_color fora do CTkFont
        ctk.CTkLabel(frame_assinatura, text="Desenvolvido por", text_color="gray", font=ctk.CTkFont(size=11)).pack()
        ctk.CTkLabel(frame_assinatura, text="Matheus Huank!", text_color="#00ff00", font=ctk.CTkFont(size=14, weight="bold")).pack()

        # ==================== ÁREA PRINCIPAL ====================
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=3) # Abas
        main_frame.grid_rowconfigure(1, weight=4) # Terminal

        # === 4 ABAS ORGANIZADAS ===
        tabview = ctk.CTkTabview(main_frame)
        tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        tab_rede = tabview.add("🌐 Rede")
        tab_reparacao = tabview.add("🧰 Reparação do Windows")
        tab_limpeza = tabview.add("🧹 Limpeza")
        tab_ferramentas = tabview.add("⚙ Ferramentas do Sistema")

        self.construir_aba_comandos(tab_rede, self.obter_comandos_rede(), tipo="cmd")
        self.construir_aba_comandos(tab_reparacao, self.obter_comandos_reparacao(), tipo="cmd")
        self.construir_aba_comandos(tab_limpeza, self.obter_comandos_limpeza(), tipo="cmd")
        self.construir_aba_comandos(tab_ferramentas, self.obter_comandos_ferramentas(), tipo="janela")

        # === TERMINAL ===
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(0, weight=1)

        self.txt_output = Text(
            output_frame, bg="#0a0a0a", fg="#00ff00", font=("Consolas", 11),
            insertbackground="white", selectbackground="#003300", wrap="word", relief="flat"
        )
        scrollbar = Scrollbar(output_frame, command=self.txt_output.yview)
        self.txt_output.configure(yscrollcommand=scrollbar.set)
        self.txt_output.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=5)

        self.status = ctk.CTkLabel(self, text="Pronto - Aguardando comando...", anchor="w")
        self.status.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        self.append_output("=== Canivete TI PRO v1.0 Iniciado ===\n", cor="cyan")

    # ====================== DICIONÁRIOS DE COMANDOS ======================
    def obter_comandos_rede(self):
        return [
            ("Mostrar IP Completo", "ipconfig /all", "Exibe detalhes das placas de rede."),
            ("Renovar IP", "ipconfig /release & ipconfig /renew", "Libera o IP e solicita um novo ao DHCP."),
            ("Limpar Cache DNS", "ipconfig /flushdns", "Limpa cache local (resolve sites não carregando)."),
            ("Ping Google", "ping 8.8.8.8", "Testa conectividade externa."),
            ("Ping Cloudflare", "ping 1.1.1.1", "Testa DNS alternativo."),
            ("Traceroute (Rotas)", "tracert -d 8.8.8.8", "Mapeia os saltos até o destino (rápido)."),
            ("Testar DNS (NSLookup)", "nslookup google.com", "Verifica resolução de nomes."),
            ("Ver Portas Abertas", "netstat -ano", "Lista conexões e portas em uso com PID."),
            ("Ver Tabela ARP", "arp -a", "Mostra IPs e MACs da rede local."),
            ("Estatísticas de Rede", "netstat -e", "Mostra pacotes enviados/recebidos e erros."),
            ("Ver Rota Padrão", "route print", "Exibe a tabela de roteamento do PC."),
            ("Resetar TCP/IP", "netsh int ip reset", "Redefine a pilha TCP/IP do Windows."),
            ("Resetar Winsock", "netsh winsock reset", "Recupera o catálogo do Winsock (salva muita internet).")
        ]

    def obter_comandos_reparacao(self):
        return [
            ("Reparar Windows (SFC)", "sfc /scannow", "Corrige arquivos corrompidos do sistema."),
            ("Restaurar Imagem (DISM)", "DISM /Online /Cleanup-Image /RestoreHealth", "Repara a imagem base do Windows."),
            ("Verificar Disco (Leitura)", "chkdsk", "Checa a integridade do disco sem travar o usuário."),
            ("Atualizar Diretivas", "gpupdate /force", "Força atualização do Active Directory (GPO)."),
            ("Informações do Sistema", "systeminfo", "Dados detalhados do SO e Hardware."),
            ("Listar Processos", "tasklist", "Exibe todos os processos rodando no momento."),
            ("Ver Drivers Instalados", "driverquery", "Lista todos os drivers do sistema."),
            ("Ver Adaptadores MAC", "getmac", "Exibe os endereços físicos (MAC) ativados."),
            ("Usuários Logados", "query user", "Lista quem está conectado na máquina."),
            ("Consultar Serviços", "sc query", "Lista o status dos serviços do Windows."),
            ("Reiniciar PC (10s)", "shutdown /r /t 10", "Reinicia a máquina com aviso de 10 segundos.")
        ]

    def obter_comandos_limpeza(self):
        return [
            ("Limpar Temp (Usuário)", r"del /q/f/s %TEMP%\*", "Remove lixo da pasta temporária do usuário atual."),
            ("Limpar Temp (Windows)", r"del /q/f/s C:\Windows\Temp\*", "Remove arquivos temporários do sistema."),
            ("Esvaziar Lixeira Forçado", r"rd /s /q C:\$Recycle.bin", "Deleta a lixeira de todas as unidades ativas."),
            ("Limpeza de Disco (UI)", "cleanmgr", "Abre o utilitário nativo de limpeza do Windows.")
        ]

    def obter_comandos_ferramentas(self):
        return [
            ("Gerenciador de Tarefas", "taskmgr", "Abre o Task Manager."),
            ("Painel de Controle", "control", "Painel de Controle clássico."),
            ("Serviços do Sistema", "services.msc", "Gerenciamento de serviços (Services.msc)."),
            ("Gerenciador de Dispositivos", "devmgmt.msc", "Controle de drivers e hardwares."),
            ("Conexões de Rede", "ncpa.cpl", "Acesso direto aos adaptadores de rede."),
            ("Editor de Registro", "regedit", "Abre o Regedit."),
            ("Visualizador de Eventos", "eventvwr", "Logs do sistema (Event Viewer)."),
            ("Desinstalar Programas", "appwiz.cpl", "Acesso rápido à remoção de softwares."),
            ("Configurações do Boot", "msconfig", "Abre o MSConfig."),
            ("Sessões SMB Ativas", "net session", "Verifica quem está conectado no PC via rede."),
            ("Pastas Compartilhadas", "net share", "Lista os compartilhamentos ativos locais."),
            ("Usuários Locais", "net user", "Lista as contas de usuário da máquina.")
        ]

    # ====================== CONSTRUTOR DE INTERFACE ======================
    def construir_aba_comandos(self, aba, lista_comandos, tipo):
        scroll_frame = ctk.CTkScrollableFrame(aba, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scroll_frame.grid_columnconfigure(0, weight=0)
        scroll_frame.grid_columnconfigure(1, weight=1)

        for i, (texto_botao, comando, descricao) in enumerate(lista_comandos):
            if tipo == "cmd":
                btn = ctk.CTkButton(scroll_frame, text=texto_botao, width=210, anchor="w", fg_color="#2b2b2b", hover_color="#404040",
                                    command=lambda c=comando: self.executar_comando(c))
            else:
                btn = ctk.CTkButton(scroll_frame, text=texto_botao, width=210, anchor="w", fg_color="#5c4d0b", hover_color="#857116",
                                    command=lambda c=comando: self.abrir_ferramenta(c))
            
            btn.grid(row=i, column=0, padx=5, pady=3, sticky="w")

            lbl = ctk.CTkLabel(scroll_frame, text=descricao, text_color="#a3a3a3", font=ctk.CTkFont(size=12))
            lbl.grid(row=i, column=1, padx=10, pady=3, sticky="w")

    # ====================== FUNÇÕES ESPECIAIS (PROVEDOR) ======================
    def auto_fix_internet(self):
        self.append_output("\n⚡ INICIANDO AUTO FIX DE INTERNET...\n", "yellow")
        comando_magico = "ipconfig /release & ipconfig /renew & ipconfig /flushdns & netsh winsock reset & netsh int ip reset"
        self.executar_comando(comando_magico)

    def diagnostico_completo(self):
        self.append_output("\n🔎 INICIANDO DIAGNÓSTICO PROFISSIONAL (Aguarde...)...\n", "yellow")
        self.atualizar_status("Gerando Relatório de Rede TXT...")
        
        tempo_agora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        nome_arquivo = f"relatorio_rede_{tempo_agora}.txt"
        caminho_txt = os.path.join(os.path.dirname(sys.executable), nome_arquivo)
        
        cmd_diag = (
            f"echo === DIAGNOSTICO COMPLETO DA REDE === > \"{caminho_txt}\" & "
            f"echo DATA/HORA: %DATE% %TIME% >> \"{caminho_txt}\" & "
            f"echo. >> \"{caminho_txt}\" & "
            f"echo [IP CONFIG] >> \"{caminho_txt}\" & ipconfig /all >> \"{caminho_txt}\" & "
            f"echo. >> \"{caminho_txt}\" & "
            f"echo [PING GOOGLE] >> \"{caminho_txt}\" & ping -n 4 8.8.8.8 >> \"{caminho_txt}\" & "
            f"echo. >> \"{caminho_txt}\" & "
            f"echo [PING CLOUDFLARE] >> \"{caminho_txt}\" & ping -n 4 1.1.1.1 >> \"{caminho_txt}\" & "
            f"echo. >> \"{caminho_txt}\" & "
            f"echo [NSLOOKUP] >> \"{caminho_txt}\" & nslookup google.com >> \"{caminho_txt}\" & "
            f"echo. >> \"{caminho_txt}\" & "
            f"echo [TRACERT] >> \"{caminho_txt}\" & tracert -d 8.8.8.8 >> \"{caminho_txt}\" & "
            f"echo. >> \"{caminho_txt}\" & "
            f"echo [INFO SISTEMA] >> \"{caminho_txt}\" & systeminfo >> \"{caminho_txt}\" & "
            f"echo. >> \"{caminho_txt}\" & "
            f"echo [TABELA ARP] >> \"{caminho_txt}\" & arp -a >> \"{caminho_txt}\" & "
            f"echo. >> \"{caminho_txt}\" & "
            f"echo [ROTAS] >> \"{caminho_txt}\" & route print >> \"{caminho_txt}\""
        )
        
        def run_diag():
            subprocess.run(cmd_diag, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.append_output(f"✅ Diagnóstico salvo com sucesso em:\n{caminho_txt}\n", "lime")
            self.atualizar_status("Pronto")
            os.startfile(caminho_txt)

        threading.Thread(target=run_diag, daemon=True).start()

    def gerar_relatorio_wmi(self):
        self.append_output("\n🔄 Coletando dados WMI...\n", "yellow")
        try:
            c = wmi.WMI()
            cpu = c.Win32_Processor()[0].Name
            ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)
            so = f"{c.Win32_OperatingSystem()[0].Caption} ({c.Win32_OperatingSystem()[0].OSArchitecture})"

            relatorio = f"""
======================================
     RELATÓRIO DO SISTEMA - {datetime.now():%d/%m/%Y %H:%M}
======================================
Máquina     : {os.getenv('COMPUTERNAME')}
Usuário     : {os.getenv('USERNAME')}
Processador : {cpu}
Memória RAM : {ram_gb} GB
Sistema     : {so}
======================================
"""
            self.append_output(relatorio, "white")
            
            tempo_agora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            nome_arquivo = f"Relatorio_Hardware_{tempo_agora}.txt"
            caminho = os.path.join(os.path.dirname(sys.executable), nome_arquivo)
            
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(relatorio)

            self.append_output(f"\n✅ Relatório salvo em: {caminho}\n", "lime")

        except Exception as e:
            self.append_output(f"\nErro WMI: {e}\n", "red")

    # ====================== FUNÇÕES BASE ======================
    def append_output(self, texto: str, cor: str = "lime"):
        def atualizar():
            self.txt_output.tag_config(cor, foreground=cor)
            self.txt_output.insert(END, texto, cor)
            self.txt_output.see(END)
        self.after(0, atualizar)

    def log(self, mensagem: str):
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(f"{datetime.now():%d/%m/%Y %H:%M:%S} - {mensagem}\n")
        except: pass

    def atualizar_status(self, texto: str):
        self.after(0, lambda: self.status.configure(text=texto))

    def executar_comando(self, comando: str):
        threading.Thread(target=self._rodar_cmd_thread, args=(comando,), daemon=True).start()

    def _rodar_cmd_thread(self, comando: str):
        self.append_output(f"\nroot@suporte:~# {comando}\n", "cyan")
        self.log(f"Executando: {comando}")
        self.atualizar_status(f"Rodando: {comando}...")

        try:
            process = subprocess.Popen(
                ["cmd.exe", "/c", comando],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding="cp850", creationflags=subprocess.CREATE_NO_WINDOW
            )

            for linha in process.stdout:
                if linha.strip(): self.append_output(linha)
            for linha in process.stderr:
                if linha.strip(): self.append_output(f"ERRO: {linha}", "red")

            process.wait()
            self.atualizar_status("Pronto")
        except Exception as e:
            self.append_output(f"\nFALHA: {e}\n", "red")
            self.atualizar_status("Erro")

    def abrir_ferramenta(self, ferramenta: str):
        self.append_output(f"\n> Abrindo {ferramenta}...\n", "yellow")
        try:
            if hasattr(os, 'startfile'):
                if "net " in ferramenta:
                    self.executar_comando(ferramenta)
                else:
                    os.startfile(ferramenta)
            else:
                subprocess.Popen(ferramenta, shell=True)
        except Exception as e:
            self.append_output(f"Erro: {e}\n", "red")

    def comando_manual(self):
        cmd = self.entry_comando.get().strip()
        if not cmd: return
        self.executar_comando(cmd)
        self.entry_comando.delete(0, END)

    def limpar_tela(self):
        self.txt_output.delete(1.0, END)
        self.append_output("=== Terminal Limpo ===\n", "cyan")


if __name__ == "__main__":
    app = SuporteToolkit()
    app.mainloop()