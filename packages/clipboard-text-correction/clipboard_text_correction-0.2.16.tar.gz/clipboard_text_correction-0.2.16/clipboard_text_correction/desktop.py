import os
import clipboard_text_correction.about as about
import subprocess

def update_desktop_database(desktop_path):
    applications_dir = os.path.expanduser(desktop_path)
    try:
        subprocess.run(
            ["update-desktop-database", applications_dir],
            check=True
        )
        print("Shortcut database updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating the database: {e}")
    except FileNotFoundError:
        print("The command 'update-desktop-database' was not found. Verify that the package 'desktop-file-utils' is installed.")



def create_desktop_file(desktop_path, overwrite=False):
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
    path = os.path.expanduser(os.path.join( desktop_path,
                                            f"{about.__linux_indicator__}.desktop"))
       
    if not os.path.exists(path) or overwrite == True:
        with open(path, "w") as f:
            f.write(desktop_entry)
        os.chmod(path, 0o755)
        print(f"File {about.__linux_indicator__}.desktop created in {path}")
        update_desktop_database(desktop_path)
    
if __name__ == '__main__':
    create_desktop_file()
