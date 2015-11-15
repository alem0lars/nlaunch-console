# Configuration ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_local_data_dir=$1
_vm_console_user=$2
_vm_console_password=$3
_vm_leveladmin_group=$4
_vm_levels_passwords=$5
_vm_console_port=$6
_vm_peda_path="/usr/share/peda"
_local_challenges_dir="${_local_data_dir}/challenges"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


echo ">> Provisioning started!"

echo ">> Installing packages.." # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
apt-get update
apt-get install -y gdb gcc git
apt-get install -y python python-virtualenv
apt-get install -y python3 python3-virtualenv
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ">> Configuring peda.." # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if [[ -d "${_vm_peda_path}" ]]; then
  cd "${_vm_peda_path}"
  git pull origin master
else
  git clone "https://github.com/longld/peda.git" "${_vm_peda_path}"
  echo "source '${_vm_peda_path}/peda.py'" > "/etc/skel/.gdbinit"
fi
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ">> Configuring vulnbox tools.." # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cp ${_local_data_dir}/vulnbox-tools/scripts/* "/usr/local/bin"
chmod +x /usr/local/bin/*
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ">> Setup NLaunch Console.." # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if [[ -z $(id -u ${_vm_console_user} 2>/dev/null) ]]; then
  useradd -m "${_vm_console_user}"
  gpasswd -a "${_vm_console_user}" ${_vm_leveladmin_group}
  echo "${_vm_console_user}:${_vm_console_password}" | /usr/sbin/chpasswd
else
  rm -R "/home/${_vm_console_user}/console"
fi
rsync -av "${_local_data_dir}/console/" "/home/${_vm_console_user}/console/" \
      --exclude ".venv"
cd "/home/${_vm_console_user}"
virtualenv -p "python3" "/home/${_vm_console_user}/console/.venv"
source "/home/${_vm_console_user}/console/.venv/bin/activate"
pip install -r "/home/${_vm_console_user}/console/requirements.txt"
deactivate
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ">> Creating NLaunch Console launcher.." # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_vm_console_launcher="/usr/local/bin/nlaunch-console"
touch "${_vm_console_launcher}"
truncate -s0 "${_vm_console_launcher}"
echo "cd '/home/${_vm_console_user}/console'"     >> "${_vm_console_launcher}"
echo "source '.venv/bin/activate'"                >> "${_vm_console_launcher}"
echo "export PORT=${_vm_console_port}"            >> "${_vm_console_launcher}"
echo "export LEVELS_PWDS=${_vm_levels_passwords}" >> "${_vm_console_launcher}"
echo "python3 main.py"                            >> "${_vm_console_launcher}"
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
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo ">> Provisioning finished!"
