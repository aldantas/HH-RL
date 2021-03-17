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
)

configs=(
	configs/default-config.ini
	)

problems=(
	VRP
	TSP
	)

agents=(
	DQN
	DMAB
	FRRMAB
	)

rewards=(
	IR
	EV
	)

acceptances=(
	ALL
	)

run() {
	problem=$1
	instance=$2
	config=$3
	agent=$4
	reward=$5
	acceptance=$6
	id=$7
	output_dir="/mnt/NAS/aldantas/HHRL"
	python runner.py -p $problem -i $instance -c $config -ag $agent -rw $reward -ac $acceptance -r $id -t 300 -o $output_dir
}

export -f run
eval 'parallel --jobs 10 --progress -u run ::: "${problems[@]}" ::: "${instances[@]}" ::: "${configs[@]}"  ::: "${agents[@]}"  ::: "${rewards[@]}"  ::: "${acceptances[@]}" ::: {1..31}'
