# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    # use ubuntu 16.04 as the base box
    config.vm.box = "generic/ubuntu1604"

    config.vm.synced_folder ".", "/vagrant", disabled: true
    config.vm.synced_folder "./Scripts", "/home/vagrant/Scripts", type: 'rsync'
    config.vm.synced_folder "./Alexa20k", "/home/vagrant/Alexa20k", type: 'rsync'
    config.vm.synced_folder "./Data", "/home/vagrant/Data", type: 'rsync'
    config.vm.synced_folder "./src", "/home/vagrant/src", type: 'rsync'

    # ssh setting
    # config.ssh.private_key_path = "~/.ssh/id_rsa"
    # config.ssh.forward_agent = true
    config.ssh.insert_key = true
    config.ssh.username = 'vagrant'
    config.ssh.password = 'vagrant'

    config.vm.network "private_network", ip: "192.168.121.5"
    config.vm.define "vm-kernel3"

    #disk size:50GB 
    config.vm.disk :disk, size: "50GB", primary: true
    config.vm.provider:"libvirt" do |lv|
      # Customize the amount of memory on the VM:
      # lv.management_network_pci_bus = "0x00"
      # lv.management_network_pci_slot = "0x05"
      lv.machine_virtual_size = 128
      lv.memory = 16384
      lv.cpus = 10
      lv.cpu_mode = "host-passthrough"
    end

    # config.vm.provision "file", source: "./kern_src", destination: "/home/vagrant/kern_src"
    # config.vm.provision "file", source: "./setup-vm.sh", destination: "/home/vagrant/setup-vm.sh"
    # config.vm.provision "shell", inline: "scripts/setup vm"
    # config.vm.provision "shell", inline: "scripts/setup antelope-vm"
    config.vm.provision "shell", inline: "Scripts/quick_dependancies.sh"
    config.vm.provision "shell", inline: "echo VM Set Up!"
end