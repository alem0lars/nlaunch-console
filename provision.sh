# Configuration ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_local_data_dir=$1
_vm_console_user=$2
_vm_console_password=$3
_vm_leveladmin_group=$4
_vm_levels_passwords=$5
_vm_console_port=$6
_vm_peda_path="/usr/share/peda"
_vm_console_base_dir="/home/${_vm_console_user}/console"
_vm_console_launcher="/usr/local/bin/nlaunch-console"
_local_challenges_dir="${_local_data_dir}/challenges"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


echo ">> Provisioning started!"

echo ">> Installing packages.." # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
apt-get update
apt-get install -y "gcc" "gdb"                        # ◀─ compiler and debugger
apt-get install -y "python"  "python-dev"  "python-virtualenv"  # ◀─ python 2
apt-get install -y "python3" "python3-dev" "python3-virtualenv" # ◀─ python 3
apt-get install -y "git"                                        # ◀─ vcs
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ">> Configuring peda.." # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if [[ -d "${_vm_peda_path}" ]]; then
  cd "${_vm_peda_path}"
  git pull origin master
else
  git clone "https://github.com/longld/peda.git" "${_vm_peda_path}"
  echo "source '${_vm_peda_path}/peda.py'" >> "/etc/skel/.gdbinit"
fi
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ">> Configuring vulnbox tools.." # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cp ${_local_data_dir}/vulnbox-tools/scripts/* "/usr/local/bin"
chmod +x /usr/local/bin/*
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ">> Setup NLaunch Console.." # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if [[ -z $(id -u ${_vm_console_user} 2>/dev/null) ]]; then
  useradd -m "${_vm_console_user}"
  [[ $(getent group "${_vm_leveladmin_group}") ]] || \
    groupadd "${_vm_leveladmin_group}"
  gpasswd -a "${_vm_console_user}" "${_vm_leveladmin_group}"
  echo "${_vm_console_user}:${_vm_console_password}" | /usr/sbin/chpasswd
else
  rm -R "/home/${_vm_console_user}/console"
fi
rsync -av "${_local_data_dir}/console/" "${_vm_console_base_dir}/" \
      --exclude ".venv"
virtualenv -p "python3" "${_vm_console_base_dir}/.venv"
source "${_vm_console_base_dir}/.venv/bin/activate"
pip install -r "${_vm_console_base_dir}/requirements.txt"
deactivate
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ">> Creating NLaunch Console launcher.." # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cat >"${_vm_console_launcher}" <<EOL
cd "/home/${_vm_console_user}/console"
export PORT="${_vm_console_port}"
export LEVELS_PWDS="${_vm_levels_passwords}"
sudo -E \
     -u "root" \
     "${_vm_console_base_dir}/.venv/bin/python3" \
     "${_vm_console_base_dir}/main.py"
EOL
chmod +x "${_vm_console_launcher}"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ">> Configuring NLaunch Challenges.." # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[[ -z $(id -u "level-001" 2>/dev/null) ]] && manage-levels create_lvl 1
cp "${_local_challenges_dir}/pyjail/pyjail.py" "/home/level-001"

[[ -z $(id -u "level-002" 2>/dev/null) ]] && manage-levels create_lvl 2
cp "${_local_challenges_dir}/hellobof/hellobof.c" "/home/level-002"
cd "/home/level-002" && \
  gcc -std=c1x -Wall -Wextra --pedantic "hellobof.c" -o "hellobof.elf" && \
  rm "hellobof.c"

[[ -z $(id -u "level-003" 2>/dev/null) ]] && manage-levels create_lvl 3
cp "${_local_challenges_dir}/goodbad/goodbad.c" "/home/level-003"
cd "/home/level-003" && \
  gcc -std=c1x -Wall -Wextra --pedantic "goodbad.c" -o "goodbad.elf" && \
  rm "goodbad.c"

[[ -z $(id -u "level-004" 2>/dev/null) ]] && manage-levels create_lvl 4

# Reset the ownership of level-001 password (it's a jail not a suid challenge).
chown "level-001:level-001" "/home/level-001/002-password"
# Suid the binaries.
chown "level-003:level-002" "/home/level-002/hellobof.elf"
chmod u+s "/home/level-002/hellobof.elf"
chown "level-004:level-003" "/home/level-003/goodbad.elf"
chmod u+s "/home/level-003/goodbad.elf"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ">> Provisioning finished!"
