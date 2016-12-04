## Assignment 4 Project Page

Steps<br>
1. ssh into the horizon vm using `ssh -i <private_key> -o StrictHostKeyChecking=no ubuntu@<floating_ip>`<br>
2. run `sudo mn -c`<br>
3. run `sudo python mr_mininet.py -p 5557 -M 10 -R 3 -r 3 energy-sorted100M.csv`<br>
4. in the mininet prompt, run `source commands.txt`to output the results in results.csv<br>