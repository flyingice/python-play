import logging


# generate finer-granularity tasks
def split_task(task):
    return []


# map_function is called once per file
def map_function(content):
    return list()


# reduce_function is called once per key
def reduce_function(key, values):
    return ""


def do_map(filename):
    try:
        with open(filename, 'rb') as infile:
            content = infile.read()
            list_key_value = map_function(content)
        # simplified model with only one reducer
        with open(get_map_filename(get_id(filename), 0), 'w') as outfile:
            for key, value in list_key_value:
                outfile.write(key + ' ' + value + '\n')

    except OSError as err:
        logging.error(err)
        raise


def do_reduce(task_number):
    try:
        map_key_value = dict()
        for i in range(task_number):
            with open(get_map_filename(i, 0), 'r') as infile:
                for line in infile:
                    key, value = line.split(' ')
                    map_key_value[key].append(value)

        for key, values in map_key_value.items():
            map_key_value[key] = reduce_function(key, values)

        with open(get_reduce_filename(0), 'w') as outfile:
            for key, value in sorted(map_key_value):
                outfile.write(key + ' ' + value + '\n')

    except OSError as err:
        logging.error(err)
        raise


def get_task_filename(seq):
    return 'task-' + str(seq)


def get_map_filename(map_seq, reduce_seq):
    return 'map-' + str(map_seq) + '-' + str(reduce_seq)


def get_reduce_filename(reduce_seq):
    return 'reduce-' + str(reduce_seq)


def get_id(filename):
    l = filename.rsplit('-', maxsplit=1)
    return l[1] if len(l) > 1 else ''
