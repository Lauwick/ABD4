# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
echo I am provisioning...
date > /etc/vagrant_provisioned_at
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: $script
  config.vm.box = "ubuntu/trusty64"
  config.vm.synced_folder "Vagrant-setup", "/mnt/bootstrap"
  config.vm.provision :shell, :path => "Vagrant-setup/bootstrap.sh"
  
  # PostgreSQL Server port forwarding
  config.vm.define "masterWrite1", primary: true do |server|
    server.vm.network "forwarded_port", guest:5432, host:15432
    server.vm.hostname = "masterWrite1.pg"
    server.vm.network "private_network", ip: "192.168.4.2"
  end
  
  config.vm.define "masterWrite2", primary: true do |server|
    server.vm.network "forwarded_port", guest:5432, host:15433
    server.vm.hostname = "masterWrite2.pg"
    server.vm.network "private_network", ip: "192.168.4.3"
  end
  
  config.vm.define "masterRead1", primary: true do |server|
    server.vm.network "forwarded_port", guest:5432, host:15434
    server.vm.hostname = "masterRead1.pg"
    server.vm.network "private_network", ip: "192.168.4.4"
  end
end


