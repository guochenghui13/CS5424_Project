# YCQL_BechMark Instruction

## Usage

**overview**: we use python to implement all transactions. 

### Prerequisites

Environment:  
* Python 3.8.10

### 0. construct porject

```shell
  git clone https://github.com/guochenghui13/cs5424
```

### 1. create relational tables.

`create_tables_command.txt` lists the SQL statments of createing tables.

### 2. load data

After you downloading the dataset, you could load it into tables by executing command in `load_data.txt`.

### 3. run the application

#### 3.1 start
To conduct experiments, just run `run_experiments.sh`. This script will assign 4 clients to a machine (totally 20 clients for 5 machines).

#### 3.2 stop
To stop running, run this script with a parameter `0`, i.e., 
```
./run_experiments.sh 0
```
### 4. get reuslts

For each test file i.txt (0 ≤ i ≤ 19), its result can be found in `./logs/log-i.txt`.

The summary of benchmark can be found in `./logs/summary.txt`
