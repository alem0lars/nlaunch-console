$data_dir          = "/vagrant_data"
$console_dir       = File.join($data_dir, "console")
$challenges_dir    = File.join($data_dir, "challenges")
$vulnbox_tools_dir = File.join($data_dir, "vulnbox-tools", "scripts")
$console_user      = "nlaunch-console"
$console_password  = "f00"
$vm_levels_passwords = "/usr/share/levels-passwords"
$levels_passwords = "/vagrant_data/data/levels-passwords.json"

$provision_script = <<PROVISION
echo ">> Provisioning started!"

apt-get update
apt-get install -y gdb gcc git
apt-get install -y python python-virtualenv
apt-get install -y python3 python3-virtualenv

echo ">> Configuring peda"
if [[ -d /usr/share/peda ]]; then
  cd "/usr/share/peda"
  git pull origin master
else
  git clone "https://github.com/longld/peda.git" "/usr/share/peda"
  echo 'source "/usr/share/peda/peda.py"' > "/etc/skel/.gdbinit"
fi

echo ">> Configuring vulnbox tools"
cp #{$vulnbox_tools_dir}/* "/usr/local/bin"
chmod +x /usr/local/bin/*

echo ">> Setup NLaunch Console"
if [[ -z $(id -u #{$console_user} 2>/dev/null) ]]; then
  useradd -m "#{$console_user}"
  echo '#{$console_user}:#{$console_password}' | /usr/sbin/chpasswd
else
  rm -R "/home/#{$console_user}/#{File.basename($console_dir)}"
fi
cp -a "#{$console_dir}" "/home/#{$console_user}"

echo ">> Configuring NLaunch Challenges"
manage-levels create_lvl 1
cp #{$challenges_dir}/pyjail/pyjail.py    /home/level-001/
manage-levels create_lvl 2
cp #{$challenges_dir}/hellobof/hellobof.c /home/level-002/
cd /home/level-002 && gcc -std=c1x -Wall -Wextra --pedantic hellobof.c -o hellobof.elf && rm hellobof.c
manage-levels create_lvl 3
cp #{$challenges_dir}/goodbad/goodbad.c   /home/level-003/
cd /home/level-003 && gcc -std=c1x -Wall -Wextra --pedantic goodbad.c -o goodbad.elf && rm goodbad.c
manage-levels create_lvl 4

echo ">> Saving levels passwords at '#{$levels_passwords}'"
[[ -f "#{$levels_passwords}" ]] && rm -R "#{$levels_passwords}"
cp "#{$vm_levels_passwords}" "#{$levels_passwords}"

echo ">> Provisioning finished!"
PROVISION



Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/vivid64"
  config.vm.box_check_update = true

  config.vm.network "private_network", ip: "10.0.20.102"

  config.vm.synced_folder ".", $data_dir

  config.vm.provider "virtualbox" do |vb|
    # Don't boot with headless mode
    vb.gui = false
    # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ["modifyvm", :id, "--memory", "2048"]
    vb.customize ["modifyvm", :id, "--cpus",   "2"]
  end

  config.vm.provision :shell, inline: $provision_script
end
