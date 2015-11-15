$provision = <<PROVISION
echo ">> Provisioning started!"

apt-get update
apt-get install gdb

cp /vagrant_data/nlaunch-challenges/pyjail/pyjail.py /home/level-001/
cp /vagrant_data/nlaunch-challenges/hellobof/hellobof.c /home/level-002/
cp /vagrant_data/nlaunch-challenges/goodbad/goodbad.c /home/level-003/

echo ">> Provisioning finished!"
PROVISION

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/vivid64"

  config.vm.box_check_update = true

  config.vm.network "private_network", ip: "10.0.20.102"

  config.vm.synced_folder ".", "/vagrant_data"

   config.vm.provider "virtualbox" do |vb|
    # Don't boot with headless mode
    vb.gui = false

    # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ["modifyvm", :id, "--memory", "2048"]
    vb.customize ["modifyvm", :id, "--cpus",   "2"]
  end

  config.vm.provision :shell, inline: $provision
end
