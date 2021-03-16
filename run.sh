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
	instance=$1
	config=$2
	agent=$3
	reward=$4
	acceptance=$5
	id=$6
	python runner.py -i $instance -c $config -ag $agent -rw $reward -ac $acceptance -t 300 -r $id
}

export -f run
eval 'parallel --jobs 10 --progress -u run ::: "${instances[@]}" ::: "${configs[@]}"  ::: "${agents[@]}"  ::: "${rewards[@]}"  ::: "${acceptances[@]}" ::: {1..31}'
