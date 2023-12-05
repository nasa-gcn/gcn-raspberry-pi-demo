# To prepare a Raspberry Pi

For _N_ = 1 to 6...

On your workstation, do the following:

1. Download, install, and launch the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) application.

2. Mount a MicroSD card.

3. In the Raspberry Pi Imager application, select the OS "Raspberry Pi OS (64-bit)".

4. Click the gear icon to select advanced options.

    a. Set hostname to "gcndemoN" where _N_ is an integer.

    b. Check "Enable SSH". Check "Allow public-key authentication only" and select your authorized keys.

    c. Check "Set username and password". Set the username to "gcndemo"; choose (and save in a secure location) a random password.

    d. Check "Set locale settings" and select your time zone and keyboard layout.

    e. Click "Save".

5. Click "Write".

On the Raspberry Pi:

1. Insert the MicroSD card. Connect a monitor, keyboard, and mouse, and boot the device.

2. Click the network icon in the task bar and set the WiFi country to US.

3. Click the network icon in the task bar and connect to Guest-CNE. You may need to open a Web browser to complete the WiFi sign on.

4. Open a terminal and make the following changes:

    a. Write the following to /etc/network/interfaces.d/eth0:

        auto eth0
        allow-hotplug eth0
        iface eth0 inet static
            address 169.254.42.N/16

    b. Write the following to /etc/ssh/sshd_config.d/linklocal.conf:

        ListenAddress 169.254.42.N

    c. Run the following:

        sudo apt-get update
        sudo apt-get update

5. Reboot the Raspberry Pi.

Make sure that you can ssh to the Raspberry Pi. Then unplug the monitor, keyboard, and mouse. Then proceed to set up the next Raspberry Pi.
