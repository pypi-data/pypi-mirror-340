import os
import clipboard_text_correction.about as about
import subprocess

DESKTOP_PATH = '~/.config/autostart'


def update_desktop_database():
    applications_dir = os.path.expanduser(DESKTOP_PATH)
    try:
        subprocess.run(
            ["update-desktop-database", applications_dir],
            check=True
        )
        print("Banco de dados de atalhos atualizado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao atualizar o banco de dados: {e}")
    except FileNotFoundError:
        print("O comando 'update-desktop-database' não foi encontrado. Verifique se o pacote 'desktop-file-utils' está instalado.")



def create_desktop_file():
    base_dir_path = os.path.dirname(os.path.abspath(__file__))
    
    home_dir = os.path.expanduser("~/")
    
    icon_path = os.path.join(base_dir_path, 'icons', 'logo.png')

    script_path = os.path.expanduser(f"~/.local/bin/{about.__linux_indicator__}")

    desktop_entry = f"""[Desktop Entry]
Type=Application
Name={about.__linux_indicator__}
Exec={script_path}
X-GNOME-Autostart-enabled=true
Icon={icon_path}
Comment={about.__description__}
Terminal=false
Path={home_dir}
Categories=Education;
StartupNotify=true
Keywords=education;python;
Encoding=UTF-8
"""
    path = os.path.expanduser(os.path.join( DESKTOP_PATH,
                                            f"{about.__linux_indicator__}.desktop"))
    
    if not os.path.exists(path):  # Evita sobrescrever
        with open(path, "w") as f:
            f.write(desktop_entry)
        os.chmod(path, 0o755)
        print(f"Arquivo .desktop criado em {path}")
        update_desktop_database()
    
if __name__ == '__main__':
    create_desktop_file()
