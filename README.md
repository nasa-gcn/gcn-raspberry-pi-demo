# Bill of Materials

| Qty | Item | Part |
| - | - | - |
| | **Electronic Components**
| 6 | Single Board Computer - Raspberry Pi 4B 8 GB | DigiKey [2648-SC0195(9)-ND](https://www.digikey.com/en/products/detail/raspberry-pi/SC0195-9/12159401) |
| 6 | LCD Display - Adafruit Mini PiTFT 1.3" | DigiKey [1528-4484-ND](https://www.digikey.com/en/products/detail/adafruit-industries-llc/4484/11503310) |
| 1 | 8-Port Ethernet Switch - Brainboxes SW-008 | DigiKey [2265-SW-008-ND](https://www.digikey.com/en/products/detail/brainboxes/SW-008/21574710) |
| 6 | DPST On/Off Rocker Switch | DigiKey [EG5600-ND](https://www.digikey.com/en/products/detail/e-switch/R5ABLKREDIF0/1805312) |
| 1 | Arcade Style SPDT Momentary Pushbutton - Red | DigiKey [1568-1476-ND](https://www.digikey.com/en/products/detail/sparkfun-electronics/COM-09336/6047815) |
| 1 | Arcade Style SPDT Momentary Pushbutton - Green | DigiKey [1568-1481-ND](https://www.digikey.com/en/products/detail/sparkfun-electronics/COM-09341/6047820) |
| 1 | Arcade Style SPDT Momentary Pushbutton - Blue | DigiKey [1568-1477-ND](https://www.digikey.com/en/products/detail/sparkfun-electronics/COM-09337/6047816) |
| 6 | USB-A Male to USB-C Male Right Angle Cable | DigiKey [189-3021108-01M-ND](https://www.digikey.com/en/products/detail/qualtek/3021108-01M/13181646) |
| 1 | DC 5V 5W Power Adapter | DigiKey [102-4120-ND](https://www.digikey.com/en/products/detail/cui-inc/SWI5-5-N-P5/6579910) |
| 18 | Insulated Female Quick Connector 24-26 AWG | DigiKey [WM18235-ND](https://www.digikey.com/en/products/detail/molex/0190030071/279036) |
| 12 | RJ45 8P8C Ethernet Plug | |
| - | Spool of Cat5 cable | |
| - | 24 AWG Insulated Wire | |
| - | Female Breadboard Pin Headers | |
| | **Spacers**
| 24 | Brass Spacer M2.5 x 6mm+6mm<span style="color: red">\*</span> | DigiKey [732-12901-ND](https://www.digikey.com/en/products/detail/würth-elektronik/971060154/9488605) |
| 6 | Brass Spacer M2.5 x 10mm+6mm<span style="color: red">\*</span> | DigiKey [732-12917-ND](https://www.digikey.com/en/products/detail/würth-elektronik/971100154/9488621) |
| 18 | Brass Spacer M2.5 x 20mm+6mm<span style="color: red">\*</span> | DigiKey [732-12949-ND](https://www.digikey.com/en/products/detail/würth-elektronik/971200154/9488653) |
| | **Fasteners**
| 24 | M2.5 Hex Nut<span style="color: red">\*</span> | McMaster [91828A113](https://www.mcmaster.com/catalog/91828A113) |
| 4 | M2.5 x 10mm Phillips Flat Head Bolt | McMaster [92010A020](https://www.mcmaster.com/catalog/92010A020) |
| 6 | M2.5 x 6mm Phillips Pan Head Bolt | McMaster [92000A104](https://www.mcmaster.com/catalog/92000A104) |
| 18 | M2.5 x 8mm Phillips Pan Head Bolt | McMaster [92000A105](https://www.mcmaster.com/catalog/92000A105) |
| 4 | M3.5 x 10mm Phillips Pan Head Bolt | McMaster [92000A155](https://www.mcmaster.com/catalog/92000A155) |
| 4 | M3.5 Hex Nut | McMaster [91828A220](https://www.mcmaster.com/catalog/91828A220) |
| 24 | M2.5 Lock Washer | McMaster [92148A070](https://www.mcmaster.com/catalog/92148A070) | |
| | **Machined Parts**
| 1 | Project Board | Fusion 360 [CAD model](https://a360.co/41hcmYX) |
| 4 | Project Board Foot | Fusion 360 [CAD model](https://a360.co/48mfR2I) |
| | **Miscellaneous**
| 1 | Pelican V525 Vault Rolling Case | Manufacturer [product page](https://www.pelican.com/us/en/product/cases/rolling-case/vault/v525)

<span style="color: red">\*</span> Rather than ordering these items individually, it is more cost-effective to purchase Qty. 3 [M2.5 Spacer Kit](https://www.amazon.com/dp/B01L06CUJG) available from Amazon.

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
