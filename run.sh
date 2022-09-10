instances=(
	0
	1
	2
	3
	4
	5
	6
	7
	8
	9
	# 10
	# 11
)

configs=(
	# configs/default-config.ini
	configs/fir_discrete.ini
	)

problems=(
	TSP
	FS
	SAT
	BP
	VRP
	PS
	)

#depois BP SW e S2 com --ow

agents=(
	DQN
	# DQNUCB
	# DMAB
	# FRRMAB
	# RAND
	# QL
	)

states=(
	# SW
	# BOLLP
	# S1
	# S2
	# S3
	# S4
	# S5
	# S6
	S7
	)

rewards=(
	# IR
	# DIV
	# IND
	# IOD
	# IOP
	RIP
	# DIP
	)

acceptances=(
	ALL
	)

run() {
	problem=$1
	instance=$2
	config=$3
	agent=$4
	state=$5
	reward=$6
	acceptance=$7
	id=$8
	output_dir="/mnt/NAS/aldantas/results_data_HHRL_states"
	python runner.py -p $problem -i $instance -c $config -ag $agent -st $state -rw $reward -ac $acceptance -r $id -t 300 -o $output_dir -ow
}

export -f run
eval 'parallel --jobs 10 --progress -u run ::: "${problems[@]}" ::: "${instances[@]}" ::: "${configs[@]}"  ::: "${agents[@]}" ::: "${states[@]}" ::: "${rewards[@]}"  ::: "${acceptances[@]}" ::: {1..31}'
