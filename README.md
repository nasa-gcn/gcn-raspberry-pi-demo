# Setup

## To prepare the Raspberry Pis

Follow these instructions for _N_ = 1 to 6 to prepare each of the 6 Raspberry Pis. On your workstation, do the following:

1. Download, install, and launch the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) application.

2. Mount a MicroSD card.

3. In the Raspberry Pi Imager application, select the OS `Raspberry Pi OS (64-bit)`.

4. Click the gear icon to select advanced options.

    a. Set hostname to <code>gcndemo<i>N</i></code> where _N_ is an integer.

    b. Check `Enable SSH`. Check `Allow public-key authentication only` and select your authorized keys.

    c. Check `Set username and password`. Set the username to `gcndemo`; choose (and save in a secure location) a random password.

    d. Check `Set locale settings` and select your time zone and keyboard layout.

    e. Click `Save`.

5. Click `Write`.

6. Remove the MicroSD card from your computer

Then, on the Raspberry Pi:

1. Insert the MicroSD card into the Raspberry Pi. Connect a monitor, keyboard, and mouse, and boot it.

2. Open a terminal and make the following changes:

    a. Write the following to /etc/network/interfaces.d/eth0:

    <pre>
    auto eth0
    allow-hotplug eth0
    iface eth0 inet static
        address 10.0.42.<i>N</i>/16</pre>

    b. Write the following to /etc/ssh/sshd_config.d/linklocal.conf:

    <pre>ListenAddress 10.0.42.<i>N</i></pre>

    c. Run the following:

        sudo apt-get update
        sudo apt-get update

5. Reboot the Raspberry Pi.

Make sure that you can ssh to the Raspberry Pi. Then unplug the monitor, keyboard, and mouse. Then proceed to set up the next Raspberry Pi.

## To configure our demo software on the Raspberry Pis

We use [Ansible](https://docs.ansible.com) to automate the rest of the setup of the Raspberry Pis.

1. Connect all 6 of the Raspberry Pis _and_ your workstation to a single Ethernet switch. Boot all of the Raspberry Pis.

2. Install Ansible on your workstation by running the command:

        pip install ansible

3. Run each of our playbooks in the following order:

        ansible-playbook -i inventory.yml playbooks/proxy.yml
        ansible-playbook -i inventory.yml playbooks/pitft.yml
        ansible-playbook -i inventory.yml playbooks/reboot.yml
        ansible-playbook -i inventory.yml playbooks/setup.yml
        ansible-playbook -i inventory.yml playbooks/clients.yml
        ansible-playbook -i inventory.yml playbooks/pitft_buttons.yml

# Operation

## Startup

1. Ensure that all rocker switches are in the "On" position.

2. Connect the power cable for the Ethernet switch to a wall outlet.

3. Connect the power cable for the USB hub to a wall outlet.

## Shutdown

1. Ensure that all rocker switches are in the "On" position.

2. Connect your workstation and run the following command to gracefully halt Raspberry Pi OS:

        ansible all -b -i inventory.yml -a poweroff

3. Wait about a minute.

4. Unplug both power cables.

## Troubleshooting

### The interactive display has frozen.

When Raspberry Pi OS is shut down and power is still suplied to the Raspberry Pi, the Mini PiTFT display will show the last image that was sent to it. If the green ACT light in the corner of the Raspberry Pi is off and/or the link lights on the Raspberry Pi's Ethernet port are off, then Raspebrry Pi OS is halted. If this is the case, then unplug and re-plug the power to the Raspberry Pi to restart it.

If Raspberry Pi is on and the display is frozen, then you can restart the program that drives the dispaly. To do this, carefully reach under the Raspberry Pi's cover with an insulating object and press the _uppermost_ of the two buttons on the Mini PiTFT to restart the display program.

### One or more Kafka brokers are never in sync.

Sometimes the Kafka broker fails to start when the system boots up. To forcibly restart the Kafka broker, carefully reach under the Raspberry Pi's cover with an insulating object and press the _lowermost_ of the two buttons on the Mini PiTFT to restart the display program.
