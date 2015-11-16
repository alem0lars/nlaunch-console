# Configuration ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$vm_data_dir = "/vagrant-data"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Vagrant.configure("2") do |config| # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  config.vm.box = "ubuntu/vivid32"
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
      "nlaunchconsole", "f00",
      "levelsadmin",                # This should be sync'd with manage-levels
      "/usr/share/levelspasswords", # This should be sync'd with manage-levels
      3000]
  end
end # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
