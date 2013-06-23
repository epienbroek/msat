RPM BUILD SYSTEM SETUP

Before building the RPM's, one has to configure the RPM
build system:
$ cat .rpmmacros
%home          %{expand:%%(cd; pwd)}
%_topdir       %{home}/rpm
%_tmppath      %{_topdir}/tmp

%debug_package %{nil}

%_signature    gpg
%_gpg_name     Allard Berends (dmsat1 env RPM signing) %<msat.disruptivefoss@gmail.com>
%_gpg_path     ~/.gnupg

The GPG private key is generated as demonstrated:
------
gpg --gen-key
gpg (GnuPG) 1.4.13; Copyright (C) 2012 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Please select what kind of key you want:
   (1) RSA and RSA (default)
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
Your selection? 2
DSA keys may be between 1024 and 3072 bits long.
What keysize do you want? (2048) 1024
Requested keysize is 1024 bits
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 
Key does not expire at all
Is this correct? (y/N) y

You need a user ID to identify your key; the software constructs the user ID
from the Real Name, Comment and Email Address in this form:
    "Heinrich Heine (Der Dichter) <heinrichh@duesseldorf.de>"

Real name: Allard Berends
Email address: msat.disruptivefoss@gmail.com
Comment: dmsat1 env RPM signing
You selected this USER-ID:
    "Allard Berends (dmsat1 env RPM signing) <msat.disruptivefoss@gmail.com>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? o
You need a Passphrase to protect your secret key.

You don't want a passphrase - this is probably a *bad* idea!
I will do it anyway.  You can change your passphrase at any time,
using this program with the option "--edit-key".

We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
++++++++++++++++++++.++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.+++++++++++++++.+++++.+++++++++++++++++++++++++.+++++>.++++++++++<+++++.....+++++

Not enough random bytes available.  Please do some other work to give
the OS a chance to collect more entropy! (Need 272 more bytes)



We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
++++++++++++++++++++++++++++++++++++++++..+++++++++++++++.++++++++++..++++++++++.++++++++++.+++++++++++++++.++++++++++++++++++++++++++++++>+++++................................+++++^^^^^^^^^
gpg: key D20130C8 marked as ultimately trusted
public and secret key created and signed.

gpg: checking the trustdb
gpg: 3 marginal(s) needed, 1 complete(s) needed, PGP trust model
gpg: depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 1u
pub   1024D/D20130C8 2013-06-23
      Key fingerprint = 5FCA BBB8 395E 50B1 ABFA  1784 AB2D 16A4 D201 30C8
uid                  Allard Berends (dmsat1 env RPM signing) <msat.disruptivefoss@gmail.com>
sub   1024g/7E2EDF0B 2013-06-23
------

Another way is to import an existing GPG key. Assume the GPG
private key is in the file gpg_key.txt, then it can be added
to the user's keyring with:
$ gpg --import ./gpg_key.txt
.. output skipped ..

It can be listed with:
$ gpg --list-keys
.. output skipped ..

The rpmbuild command must be available. Check it with:
$ rpmbuild
rpmbuild: no spec files given for build

Make the rpmbuild directories:
$ mkdir -p ~/rpm/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}


BUILD ORGANIZATION WITH BUILD.SH

In order to build the RPM's in the subdirectories, one has
to go the container directory of the RPM and run the
build.sh script.

Every RPM container directory has a build.sh. Once, in the
directory, run:
$ ./build.sh
..outpud skipped ..

To build everything at once, use the build_all.sh script. It
can be called from any directory with
./build_all.sh.


EXAMPLE BUILD.SH RUN

$ cd .../msat/custom-rpms/conf-rpms-5/ds_setup
$ ./build.sh 
Building target platforms: noarch
Building for target noarch
Executing(%prep): /bin/sh -e /home/allard/rpm/tmp/rpm-tmp.7vq0hX
+ umask 022
+ cd /home/allard/rpm/BUILD
+ cd /home/allard/rpm/BUILD
+ rm -rf ds_setup
+ /usr/bin/gzip -dc /home/allard/rpm/SOURCES/ds_setup.tar.gz
+ /usr/bin/tar -xf -
+ STATUS=0
+ '[' 0 -ne 0 ']'
+ cd ds_setup
+ /usr/bin/chmod -Rf a+rX,u+w,g-w,o-w .
+ exit 0
Executing(%build): /bin/sh -e /home/allard/rpm/tmp/rpm-tmp.DQBwG3
+ umask 022
+ cd /home/allard/rpm/BUILD
+ cd ds_setup
+ exit 0
Executing(%install): /bin/sh -e /home/allard/rpm/tmp/rpm-tmp.6pMk79
+ umask 022
+ cd /home/allard/rpm/BUILD
+ cd ds_setup
+ rm -rf /home/allard/rpm/BUILDROOT/ds_setup-1.0.0-0.noarch
+ mkdir -p /home/allard/rpm/BUILDROOT/ds_setup-1.0.0-0.noarch/usr/share/doc/ds_setup
+ mkdir -p /home/allard/rpm/BUILDROOT/ds_setup-1.0.0-0.noarch/root
+ install README /home/allard/rpm/BUILDROOT/ds_setup-1.0.0-0.noarch/usr/share/doc/ds_setup
+ install setup.inf /home/allard/rpm/BUILDROOT/ds_setup-1.0.0-0.noarch/root
+ /usr/lib/rpm/brp-compress
+ /usr/lib/rpm/brp-strip /usr/bin/strip
+ /usr/lib/rpm/brp-strip-static-archive /usr/bin/strip
+ /usr/lib/rpm/brp-strip-comment-note /usr/bin/strip /usr/bin/objdump
Processing files: ds_setup-1.0.0-0.noarch
Requires(interp): /bin/sh /bin/sh /bin/sh /bin/sh
Requires(rpmlib): rpmlib(CompressedFileNames) <= 3.0.4-1 rpmlib(PayloadFilesHavePrefix) <= 4.0-1
Requires(pre): /bin/sh
Requires(post): /bin/sh
Requires(preun): /bin/sh
Requires(postun): /bin/sh
Checking for unpackaged file(s): /usr/lib/rpm/check-files /home/allard/rpm/BUILDROOT/ds_setup-1.0.0-0.noarch
Wrote: /home/allard/rpm/RPMS/noarch/ds_setup-1.0.0-0.noarch.rpm
Executing(%clean): /bin/sh -e /home/allard/rpm/tmp/rpm-tmp.XoqeFn
+ umask 022
+ cd /home/allard/rpm/BUILD
+ cd ds_setup
+ exit 0
Executing(--clean): /bin/sh -e /home/allard/rpm/tmp/rpm-tmp.x9mVtu
+ umask 022
+ cd /home/allard/rpm/BUILD
+ rm -rf ds_setup
+ exit 0


MAKING GIT USER RECOGNIZABLE

One can set the name and email address as is done in the
following example:
The configuration will be stored in ~/.gitconfig:
$ git config --global user.name "Allard Berends"
$ git config --global user.email "msat.disruptivefoss@gmail.com"
$ git config --global core.editor vim
$ git config --global merge.tool vimdiff

Now, one can see with "git log" in a repository which user
(author) made changes.
