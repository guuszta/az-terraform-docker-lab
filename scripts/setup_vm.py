#!/usr/bin/env python3
import shutil
import subprocess
import tarfile
import urllib.request
from pathlib import Path

# Variáveis de versão e caminhos
VERSION = "1.8.2"
FILENAME = f"node_exporter-{VERSION}.linux-amd64"
URL = f"https://github.com/prometheus/node_exporter/releases/download/v{VERSION}/{FILENAME}.tar.gz"
TMP_DIR = Path("/tmp")
TAR_PATH = TMP_DIR / f"{FILENAME}.tar.gz"


def run_cmd(command: list[str]) -> None:
    """Executa comandos do Linux e interrompe o script se algo falhar (check=True)."""
    subprocess.run(command, check=True)


def install_node_exporter() -> None:
    # 1. Download do pacote oficial
    print(f"Baixando Node Exporter v{VERSION}...")
    urllib.request.urlretrieve(URL, TAR_PATH)

    # 2. Extração com context manager ('with' fecha o arquivo automaticamente)
    print("Extraindo arquivos...")
    with tarfile.open(TAR_PATH, "r:gz") as tar:
        tar.extractall(path=TMP_DIR)

    # 3. Move o binário para /usr/local/bin e ajusta permissão de execução
    binary_source = TMP_DIR / FILENAME / "node_exporter"
    binary_dest = Path("/usr/local/bin/node_exporter")
    shutil.move(str(binary_source), str(binary_dest))
    binary_dest.chmod(0o755)

    # 4. Cria usuário dedicado sem login interativo
    run_cmd(["useradd", "--no-create-home", "--shell", "/bin/false", "node_exporter"])
    shutil.chown(binary_dest, user="node_exporter", group="node_exporter")

    # 5. Escreve a unit do systemd usando Path.write_text()
    service_content = """[Unit]
Description=Prometheus Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
"""
    Path("/etc/systemd/system/node_exporter.service").write_text(service_content)

    # 6. Recarrega o systemd, inicia o serviço e limpa o /tmp
    run_cmd(["systemctl", "daemon-reload"])
    run_cmd(["systemctl", "enable", "--now", "node_exporter"])

    TAR_PATH.unlink(missing_ok=True)
    shutil.rmtree(TMP_DIR / FILENAME, ignore_errors=True)
    print("Node Exporter instalado e rodando na porta 9100!")


if __name__ == "__main__":
    install_node_exporter()
