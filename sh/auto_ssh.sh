#!/usr/bin/expect -f

#set port port_no
set user [lindex $argv 0]
set host [lindex $argv 1]
set password  [lindex $argv 2]
set timeout -1

spawn ssh $user@$host
expect "*assword:*"

send "$password\r"
interact
~         
