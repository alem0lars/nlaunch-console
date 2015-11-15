
$console_dir       = File.join($data_dir, "console")
$console_venv_dir  = File.join($console_dir, ".venv")
$challenges_dir    = File.join($data_dir, "challenges")
$vulnbox_tools_dir = File.join($data_dir, "vulnbox-tools", "scripts")
$console_user      =
$console_password  =
$vm_levels_passwords = "/usr/share/levels-passwords"
$levels_passwords = "/vagrant_data/data/levels-passwords.json"

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/vivid64"
  config.vm.box_check_update = true

  config.vm.network "private_network", ip: "10.0.20.102"

  config.vm.synced_folder ".", $vm_data_dir

  config.vm.provider "virtualbox" do |vb|
    # Don't boot with headless mode
    vb.gui = false
    # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ["modifyvm", :id, "--memory", "2048"]
    vb.customize ["modifyvm", :id, "--cpus",   "2"]
  end

  config.vm.provision :shell do |s|
    s.path = "provision.sh"
    s.args = [
      $vm_data_dir,
      "nlaunch-console",
      "f00"
    ]
  end
end
