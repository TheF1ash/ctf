# Pickle Rick (Easy)
This Rick and Morty themed challenge requires you to exploit a webserver to find 3 ingredients that will help Rick make his potion to transform himself back into a human from a pickle.

Deploy the virtual machine on this task and explore the web application.

On deploying the machine, I got the following IP for the box: `10.10.184.179`

Lets first start with the enumeration of the box.

**Nmap Scan and results**
```
Nmap scan report for ip-10-10-184-179.eu-west-1.compute.internal (10.10.184.179)
Host is up, received arp-response (0.0036s latency).
Scanned at 2021-05-15 20:31:38 BST for 8s
Not shown: 998 closed ports
Reason: 998 resets
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 64 OpenSSH 7.2p2 Ubuntu 4ubuntu2.6 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 64 Apache httpd 2.4.18 ((Ubuntu))
MAC Address: 02:AC:3E:50:67:9D (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
So we see ports 22(SSH) and 80(HTTP) are open.

**Analyzing the Website**
Lets look at the website.
We go to `http://10.10.184.179` and are greeted with the following webpage:
![Tryhackme Pickle Rick Website](website.png "TryHackme Pickle Rick Website")
Here we can see that on the webpage it says '**BURRRP**' and emphasises that

So its a hint to use Burp to analyze the website
Now lets see the source code of the webpage.
In the webpage source code we can see this comment:
```
 <!--

    Note to self, remember username!

    Username: R1ckRul3s
  
  -->
```
So we have a username, most likely for the SSH to the machine.

Before analyzing further with Burp, lets head to gobuster and fuzz for the directories on the page:

```
gobuster dir -u http://10.10.184.179 -w /usr/share/wordlists/dirb/big.txt -t 10
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.184.179
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2021/05/15 21:52:49 Starting gobuster
===============================================================
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/assets (Status: 301)
/robots.txt (Status: 200)
/server-status (Status: 403)
===============================================================
2021/05/15 21:52:52 Finished
===============================================================
```
A robots.txt file? Lets see what it has.
On opening robots.txt, we see it just has some text 'Wubbalubbadubdub'. I have no clue what that means at this time, but searching it on a browser gives us the result that it is Rick's catchphrase, as a joke.
Could it be the password for the SSH login?
Trying to SSH with username `R1ckRul3s` as below:
```
root@ip-10-10-63-226:~# ssh R1ckRul3s@10.10.184.179
The authenticity of host '10.10.184.179 (10.10.184.179)' can't be established.
ECDSA key fingerprint is SHA256:3IZOS+bZfsFaIe8DgNSZoH2TRVaGhndV3SLdgwzY/YA.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.10.184.179' (ECDSA) to the list of known hosts.
R1ckRul3s@10.10.184.179: Permission denied (publickey).
```
We get a permission denied (publickey) error which means it is likely expecting a private key for SSH login.

However, that doesnt seem much useful at this time. So lets proceed to analyzing with Burp.
In Burp while intercepting requests on the main page I didnt notice anything interesting in the headers or anywhere.
At this point we dont have much to go forward with.
Then lets try Nikto:
```
nikto -h 10.10.184.179
- Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.10.184.179
+ Target Hostname:    ip-10-10-184-179.eu-west-1.compute.internal
+ Target Port:        80
+ Start Time:         2021-05-15 22:19:11 (GMT1)
---------------------------------------------------------------------------
+ Server: Apache/2.4.18 (Ubuntu)
+ Server leaks inodes via ETags, header found with file /, fields: 0x426 0x5818ccf125686 
+ The anti-clickjacking X-Frame-Options header is not present.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ "robots.txt" retrieved but it does not contain any 'disallow' entries (which is odd).
+ Allowed HTTP Methods: OPTIONS, GET, HEAD, POST 
+ Cookie PHPSESSID created without the httponly flag
+ OSVDB-3233: /icons/README: Apache default file found.
+ /login.php: Admin login page/section found.
+ 6544 items checked: 0 error(s) and 7 item(s) reported on remote host
+ End Time:           2021-05-15 22:19:21 (GMT1) (10 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested

```
As we can see, it found an admin login page. There we can see that there is a page with username and password fields for input. Lets try the username `R1ckRul3s` and the string `Wubbalubbadubdub` from robots.txt as the password here.

And it works!!!!
We are now on a portal.php page, with a command panel. We can probably type commands for executing on the server here.
Issuing the `ls` command in the command panel listed the files:
![Tryhackme Pickle Rick Portal](command_panel.png "TryHackme Pickle Rick Portal")

And it seems that `Sup3rS3cretPickl3Ingred.txt` might contain, like its name suggests, the name of a super secret pickle ingredient. Lets do a `cat Sup3rS3cretPickl3Ingred.txt`. 
We see the following error on doing the `cat Sup3rS3cretPickl3Ingred.txt` command.
![Tryhackme Pickle Rick Cat Command Error](cat_error.png "TryHackme Pickle Rick Portal")

So it seems they have blocked cat command to list file contents. Anyways, lets try the `tac` command which lists the file contents, but in reverse, like `tac Sup3rS3cretPickl3Ingred.txt` and there we have it! The first ingredient!

### Question 1: What is the first ingredient Rick needs?
**Answer**: `mr. meeseek hair`

Now proceeding further, we can try to look for the other ingredient. Lets list the file contents again. 
![Tryhackme Pickle Rick Portal](command_panel.png "TryHackme Pickle Rick Portal")

Lets see what `clue.txt` contains. `tac clue.txt` in the command panel gives us `Look around the file system for the other ingredient.`.
So lets try to browse through the file system and see if we can see anything interesting.
Lets try to see if we can navigate up to /home
And we are. If we do `ls ../../../home/` we see that there is a `rick` directory, for user `rick`
And we can do `ls ../../../home/rick` and see that it lists a file, `second ingredients`. Now we can try do `tac ../../../home/rick/second ingredients`, but that wont work because the filename contains spaces. It will try to do `tac` on `second` followed by `ingredients`, but it will fail because there are no such files in the directory.
So the correct way to `tac` the file is to use quotes in the filename, like 'second ingredients'. So the correct syntax will be `tac 'second ingredients'`.
Issuing this command gives us the second ingredient.

### Question 2: Whats the second ingredient Rick needs?
**Answer**: `1 jerry tear`

Now we just have 1 more ingredient to find. Looking at the filesystem further doesnt help much because there is nothing much interesting in the `/home/rick` directory or even the `/home/ubuntu` directory which we can read.

**Rabbit Hole Ahead**
I went back to view the page source for `portal.php` and there I could see what looked like a base64 encoded string in the comment, `Vm1wR1UxTnRWa2RUV0d4VFlrZFNjRlV3V2t0alJsWnlWbXQwVkUxV1duaFZNakExVkcxS1NHVkliRmhoTVhCb1ZsWmFWMVpWTVVWaGVqQT0==`. I tried base64 decoding this at base64decode.org, but it failed saying malformed input. Then I removed one '=' sign from the end, and it decoded further, to another base64 string. Then I continued decoding further, until I found the following string at the end: `rabbit hole`, which means this was a rabbit hole, and not the actual answer. 

**The End**
I was stuck at the third flag for some time. And finally gave up and looked up John Hammond's video writeup of this, and want to point out that I tried using netcat to get a reverse shell but failed. So I gave up, instead maybe I should have tried using a python reverse shell. Anyways, I learned to explore more ways to have a reverse shell and not give up early. You can check out the other writeups for how they do it for the third question.
