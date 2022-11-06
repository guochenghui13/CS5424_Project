#!/bin/bash
run_experiment() {
    mv ~/ycql_scripts/logs/*.txt ~/ycql_scripts/logs/backup/

    if (( $1 == 0 ))
    then
        line=2
        for ((i=0; i<5; i++))
        do
            machine_name="xcnd$((30 + $i % 5))"
            ~/.local/usr/bin/sshpass -p +rW8FLp3 ssh -q cs4224n@$machine_name.comp.nus.edu.sg "ps -ef | grep driver.py | awk '{print \$$line}' | xargs kill -9" 
        done
    else
        for ((i=0; i<20; i++))
        do 
            machine_name="xcnd$((30 + $i % 5))"
            echo "Assigning $machine_name to client $i"
            file_name="~/sql_test/project_files/xact_files/$i.txt"
            echo $file_name
            # nohup ~/.local/usr/bin/sshpass -p +rW8FLp3 ssh -q cs4224n@$machine_name.comp.nus.edu.sg "~/ycql_scripts/ && python driver.py ~/sql_test/project_files/xact_files/$i.txt" &
            ~/.local/usr/bin/sshpass -p +rW8FLp3 ssh -q cs4224n@$machine_name.comp.nus.edu.sg "cd ~/ycql_scripts/ && nohup python -u driver.py ~/sql_test/project_files/xact_files/$i.txt > ~/ycql_scripts/logs/log-$i.txt" &
        done
    fi
}

run_experiment $1