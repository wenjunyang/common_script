#!/usr/bin/expect -f  
  
#set port port_no  
set user ${user}
set host ${host}
set password ${pd}
set timeout -1  
  
spawn ssh $user@$host  
expect "*assword:*"  
  
send "$password\r"  

#进入交互模式
interact 
