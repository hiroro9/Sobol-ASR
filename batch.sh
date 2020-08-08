#!/bin/sh

EXP="ASR-K-G.py"

expect -c "
spawn python $EXP

expect \"n1\"
send \"1\n\"
expect \"n2\"
send \"0\n\"
expect \"n3\"
send \"0\n\"

exit 0
"

expect -c "
spawn python $EXP

expect \"n1\"
send \"0\n\"
expect \"n2\"
send \"1\n\"
expect \"n3\"
send \"0\n\"

exit 0
"

expect -c "
spawn python $EXP

expect \"n1\"
send \"0\n\"
expect \"n2\"
send \"0\n\"
expect \"n3\"
send \"1\n\"

exit 0
"

expect -c "
spawn python $EXP

expect \"n1\"
send \"1\n\"
expect \"n2\"
send \"1\n\"
expect \"n3\"
send \"0\n\"

exit 0
"

expect -c "
spawn python $EXP

expect \"n1\"
send \"1\n\"
expect \"n2\"
send \"0\n\"
expect \"n3\"
send \"1\n\"

exit 0
"
expect -c "
spawn python $EXP

expect \"n1\"
send \"0\n\"
expect \"n2\"
send \"1\n\"
expect \"n3\"
send \"1\n\"

exit 0
"


